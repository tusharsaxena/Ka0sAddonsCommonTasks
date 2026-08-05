# 02 — Upstream Changes (Milestone 1)

**Every change to LibKa0s, WowAddonStandards and the `wow-addon` plugin, in one place.**

Nothing here has been executed. See `00_OVERVIEW.md`.

---

## Why Milestone 1 exists and is upstream-only

Three repositories own the root cause of 21 of the 33 clusters. Fixing those clusters in the addons
first produces work that is either wrong (writing `docs/performance.md` for a harness that was
deliberately not adopted), impossible (there is no honest way to skip a test case — `Kit.skip` does not
exist), or reverted on the next re-vendor (a British-spelling patch inside `libs/LibKa0s/`).

The rule this plan is built on: **nothing in Milestone 2 or later may depend on an upstream change that
is not in Milestone 1.** Every upstream edit is here. `04_EXECUTION_PLAN.md` then sequences adoption
against these ids and nothing else.

**Milestone 2 has zero Milestone-1 dependencies** and can be executed in parallel — it is the eight
Highs, and they are local defects.

### The three upstream repositories

| Repo | Path | Role |
|---|---|---|
| LibKa0s | `/mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s` | The shared library **and** the shared test kit, both vendored into every addon. |
| WowAddonStandards | `/mnt/d/Profile/Users/Tushar/Documents/GIT/WowAddonStandards` | The standard (v2.21.0) and the three playbooks. |
| wow-addon | `/mnt/d/Profile/Users/Tushar/Documents/GIT/wow-addon` | The plugin: 16 commands and 2 agents that read the playbooks and act on addon repos. |

### Milestone 1 at a glance

| Group | Items | Clusters unblocked | Findings closed here | Findings unblocked downstream |
|---|---|---|---|---|
| LibKa0s (`M1-LK-01` … `M1-LK-14`, plus conditional `M1-LK-15`) | 14 (+1) | C2, C6, C8, C9, C12, C13, C15, C18, C21, C27, C33 | 20 | ~55 |
| WowAddonStandards (`M1-STD-01` … `M1-STD-17`) | 17 | C1, C2, C4, C5, C6, C8, C9, C11, C12, C13, C15, C17, C18, C20 | 2 | ~90 |
| wow-addon plugin (`M1-WA-01` … `M1-WA-10`) | 10 | C1, C3, C4, C5, C8, C15, C18 | 0 | ~40 |

**41 items** (42 under `M1-STD-11` option (b), which schedules `M1-LK-15`).

**Twenty-two** findings are closed *inside* Milestone 1 — LibKa0s's own nineteen, plus `PC-R-07` (a defect
in the vendored runner, fixed at the source), plus the two rule-text problems whose resolution **is** the
rule change (`PC-A-12` via `M1-STD-12`, `PC-A-22` via `M1-STD-15`). The rest are unblocked, not closed.
`AT-A-10` was in this count in an earlier draft; it is now an `M3-08` register row (see `M1-STD-12`).

---

## Ordering inside Milestone 1

```
M1-STD-16 (version rollup) ── last, after every other STD item
      ▲
      └── M1-STD-01 … M1-STD-15, M1-STD-17
            most are independent of each other, but FOUR are not:
              M1-STD-10 ← M1-STD-03   (needs Kit.skip named)
              M1-STD-13 ← M1-STD-02   (needs the register)
              M1-STD-15 ← M1-STD-08   (needs the citation rule)
              M1-STD-16 ← all fifteen + M1-STD-17

M1-LK-01 (Kit.skip) ──┬── M1-LK-02 (vendor_sync module)
                      └── M1-LK-04 (suite inventory)
M1-LK-03 (xmlFiles)  ──┴── M1-LK-11 (LibKa0s adopts both)
M1-LK-05, -06, -07, -09, -10, -12  (independent)
M1-LK-08  ← depends on M1-STD-14
M1-LK-13  ← depends on M1-STD-07
M1-LK-15  ← CONDITIONAL on M1-STD-11 choosing (b)
M1-LK-14 (cut v1.8.0) ← LAST in Group A, after M1-LK-01…13 (+15 under (b))

M1-WA-01, -05, -06, -08  (independent)
M1-WA-02 ← M1-STD-05     (so the sweep's target wording is normative)
M1-WA-03 ← M1-STD-17     (or AUDIT.md overrides it at runtime)
M1-WA-04 ← M1-STD-02
M1-WA-07 ← M1-STD-08
M1-WA-09 ← M1-STD-09     (so the report cites a resolved rule)
M1-WA-10 ← M1-WA-07, and sequenced AFTER M4-10
```

**So Group A and Group C are not parallel with Group B.** Two Group A items (`M1-LK-08`, `M1-LK-13`) and
five Group C items (`M1-WA-02`, `-03`, `-04`, `-07`, `-09`) each wait on a specific `M1-STD-*`. Group B
leads; the rest of Milestone 1 follows it. The only thing that is **unconditionally** parallel from day one
is **Milestone 2**.

`M1-LK-01` … `M1-LK-07` **must ship as one kit revision**, so a consumer takes one re-vendor rather than
four. `Kit.VERSION` goes 7 → 8 once, with one `docs/api/testkit/version-8-docs.md`.

---

# Group A — LibKa0s

Path: `/mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s`

---

## M1-LK-01 · `Kit.skip(reason)` in the test kit

**File / symbol:** `testkit/framework.lua` — new `Kit.skip`, changes to `Kit.run` (`:188-200`),
`renderInventory` (`:136-170`), `Kit.expose` (`:75-87`), `Kit.VERSION` (`:20`, 7 → 8).
New: `docs/api/testkit/version-8-docs.md`.

**Verified problem.** `testkit/framework.lua` offers `assertEqual`/`assertTrue`/`assertFalse`/`assertNil`/
`assertNear`/`assertError` and nothing else; `Kit.run` counts every case as exactly pass or fail. A grep
for `skip` in that file returns one hit — a comment at `:99` describing `loadSuites` swallowing a missing
file. The shell half already speaks the word: `testkit/run-automated-tests.sh` carries a suite-level
`skip` status with a reason at five sites. Six repos therefore forged a case-level skip out of a bare
`return`, which registers as PASS.

**Change.** Implement as a sentinel error so it works from inside a case body without restructuring the
case:

```lua
local SKIP = {}
function Kit.skip(reason) error(setmetatable({ reason = reason }, SKIP), 0) end
```

`Kit.run` branches on the sentinel: a skipped case increments a third counter, prints
`  SKIP  <name> — <reason>`, and the tail line becomes `%d passed, %d failed, %d skipped, %d total`.

Two properties are non-negotiable:

- **A skip MUST NOT be folded into `passed`.** The `[tests]` badge and `docs/test-cases.md` count passes.
- **A skip MUST NOT change the exit code.** `framework.lua:200` stays `failed == 0`, because the same
  script is the commit gate and the release gate reads `suites.tests.failed` from the manifest.

`renderInventory` renders a skipped case with a `(skipped: reason)` suffix, so the generated inventory
discloses it — that is the half `testing-§12` actually cares about.

**Findings unblocked:** C6 in full — `AT-R-13`, `BL-R-02`, `BL-A-14`, `CM-R-07`, `CM-A-31`, `KCD-R-02`,
`KCD-A-12`, `LH-R-05`, `LH-A-40`, `PM-R-05` (10). Also enables `M1-LK-04`/`M1-STD-10`.

**Adoption cost downstream.** Additive — a consumer on kit 7 keeps working. Each of the six repos
re-vendors `tests/_kit/` and edits two lines in `tests/test_vendor_sync.lua`, then regenerates
`docs/test-cases.md`. Pass counts do not move, so no README badge changes. ConsumableMaster and KickCD
gain nothing until `M3-10` (their runners never load the kit). LibKa0s itself must re-vendor into
`tests/_kit/` or `tests/test_kitsync.lua` reddens.

**Effort:** S · **Risk:** low.

---

## M1-LK-02 · `testkit/vendor_sync.lua` — one gate, not six copies

**File / symbol:** new `testkit/vendor_sync.lua` exporting `VendorSync.register(T, opts)`.
Moves `readBytes`, `gitOut`, `gitShow`, `shippedNames`, `localNames`, `bundledVersion`, `siblingTag`,
`assertVendorSync` in verbatim.

**Verified problem.** The consumer-side gate is ~150 lines copy-pasted into six repos with a one-line
delta (`local T = _G.AT_TEST` versus `_G.LH_TEST`). Every copy carries the same vacuous PASS and the same
false header claiming the skip "is said in the case name" when neither case name mentions it. Six copies
means six chances to fix `M1-LK-01` six different ways.

**Change.** A factory rather than auto-registration, so a consumer keeps ownership of its case names and
its test global:

```lua
local VendorSync = dofile("tests/_kit/vendor_sync.lua")
VendorSync.register(T, {
  root = ".", sibling = "../LibKa0s", readmePattern = ...,
  pairs = { { tag = "LibKa0s", local_ = "libs/LibKa0s" },
            { tag = "testkit", local_ = "tests/_kit" } },
})
```

`if not tag then return end` becomes
`Kit.skip("../LibKa0s checkout absent — the vendored payload was not compared")`.
**The comparison contract, stated exactly, because an earlier draft of this document got it backwards.**
The consumer-side gate compares a **working-tree file** against a **`git show` blob**, and those two are
not in the same representation: the blob is LF
(`git -C LibKa0s show HEAD:LibKa0s/Core.lua | tr -cd '\r' | wc -c` → **0**) while every consumer's working
tree is CRLF (`tr -cd '\r' < AbsorbTracker/libs/LibKa0s/Core.lua | wc -c` → **322**), because eight of the
nine repos pin `text=auto eol=crlf` or `*.lua text eol=crlf` in `.gitattributes`. So `vendor_sync.lua`
compares raw bytes read in binary mode with **exactly one** normalization — **CR stripped from the
working-tree side, and nothing else** — which compares the file to the blob it round-trips to.
AbsorbTracker's existing gate documents this at `tests/test_vendor_sync.lua:28-32` and the header MUST be
carried in verbatim. The normalization-free alternative, and the better one if the module is rewritten
rather than moved, is `git hash-object <local file>` against the sibling's blob sha — git does the
round-trip itself. A real fork in content still fails under either. **Do not remove
`ConsumableMaster/tests/test_vendor_sync.lua:133`'s `gsub`**; it is correct, and every other copy has the
same line. `M1-STD-03` scopes `testing-§11`'s no-normalization MUST to the library-side pair, where both
sides are working-tree directories in one checkout.

Two properties worth stating in the module header: the gate now lives *inside* the payload it checks, so
a locally patched copy fails its own byte-identity assertion; and LibKa0s cannot run it (no sibling),
which is why `register` is called by the consumer and `tests/test_kitsync.lua` stays the library-side
equivalent.

**Findings unblocked:** the same C6 ten, plus it is the vehicle that makes the `M1-LK-01` fix land once
instead of six times.

**Adoption cost downstream.** Six repos rewrite `tests/test_vendor_sync.lua` as a ~10-line call and delete
~140 lines each; **case names must stay the same** so `docs/test-cases.md` counts do not move. WhatGroup
and prettychat have no vendor-sync gate at all (`ls WhatGroup/tests/test_vendor_sync.lua` → absent, same
for prettychat) and gain one for the first time.

**Checked, so the adoption is not a surprise:** both new gates read the provenance line out of `README.md`
with the pattern `[Bb]undles %[LibKa0s%]%b() (v[%d%.]+)`, which accepts mid-sentence, lowercase forms —
that leniency is already in the shipped gate precisely because LootHistory writes it that way. Executed
against WhatGroup's `README.md:83` ("…it bundles [LibKa0s](…) v1.7.0 (MIT), the shared Ka0s library…") the
pattern returns `v1.7.0`, and prettychat's `README.md:122` is the canonical sentence. So neither repo needs
a `readmePattern` override and neither is expected to redden on the provenance line. What both gates *will*
compare is bytes-against-tag, which is why `M3-01` re-vendors **both** payloads and bumps the provenance
line in the same commit.

**Sequencing trap, stated explicitly.** The gate compares *file sets*. The first re-vendor lands
`tests/_kit/vendor_sync.lua` while the OLD in-repo gate is still running, so the new file must appear on
both sides at the same tag: **re-vendor and rewrite are one commit**, against a LibKa0s tag that already
carries the file.

**Effort:** M · **Risk:** medium.

---

## M1-LK-03 · `Loader.xmlFiles(xmlPath)`

**File / symbol:** `testkit/loader.lua` — new `Loader.xmlFiles`, placed immediately after
`Loader.tocFiles` (`:74-88`).

**Verified problem.** `LibKa0s/LibKa0s.xml` lists eight `<Script file="…"/>` entries in dependency order.
Every consuming runner re-types it: `AbsorbTracker/tests/run.lua:21-30` **and** `tests/perf.lua:61` (twice
in one repo), `BankLedger/tests/run.lua:32`, `ConsumableMaster/tests/loader.lua:49`,
`KickCD/tests/loader.lua:29`, `prettychat/tests/loader.lua:32-40`, `PanelMaster/tests/run.lua:24-31`, and
`LibKa0s/tests/run.lua:17-19`. PanelMaster's copy names six of eight — `Perf.lua` and `PerfPanel.lua` are
absent — and nothing noticed. `Loader.tocFiles`'s own comment names the gap: "vendored libraries are
pulled in through their own XML, which this cannot see, so runners prepend their own explicit lib list."

**Change.** Mirror `tocFiles`'s contract: open the file, match `file%s*=%s*["']([^"']+)["']` per line,
skip comments, and return forward-slash paths **prefixed with the XML's own directory** so the result is
directly loadable (`libs/LibKa0s/Core.lua`, not `Core.lua`). The prefixing is the whole ergonomic
difference between a helper runners adopt and one they wrap. Error with the same "tests run from the
repo root" message on a missing file, so a typo'd path fails loudly instead of yielding an empty list
that loads nothing and reads as a clean run.

**Findings unblocked:** `PM-A-10`, and it is the prerequisite for `M1-LK-11` (LibKa0s's own `LK-R-01`,
`LK-A-09`) and for `M3-03` (`AT-R-05`, `CM-A-03`, `LH-A-29`).

**Adoption cost downstream.** Purely additive. Nine repos each delete an 8-entry literal for one call;
AbsorbTracker deletes two. **PanelMaster's list silently grows from six to eight**, loading `Perf.lua`
and `PerfPanel.lua` into its harness for the first time — that is the point, but PM should expect its
suite to move. prettychat and ConsumableMaster keep their `tests/loader.lua` wrappers and change only
the list inside them.

**Honest limit.** This removes the duplication and makes `PM-A-10`'s class impossible. It does not by
itself assert that the runner *fed* what it derived — that is `M1-LK-04`.

**Effort:** S · **Risk:** low.

---

## M1-LK-04 · `loadSuites` refuses to skip silently; `Kit.assertSuiteInventory`

**File / symbol:** `testkit/framework.lua` — `loadSuites` (`:101-110`), new `Kit.assertSuiteInventory(dir, suites)`,
new `opts.suiteInventory` in `Kit.run`.

**Verified problem.** `framework.lua:101-108` skips a `SUITES` entry naming a file that is not on disk,
and the comment at `:99` calls it deliberate — "so a suite can be listed while it is being written
without taking the whole run down with it." That convenience is why both of `testing-§9`'s silent failure
modes are live: a renamed or deleted suite is skipped rather than failed, and a new suite file nobody
added to the list never runs.

**Change.**
- `loadSuites` raises on a declared suite whose file is absent, naming the path and its position in the
  suites list.
- The written-in-progress case is preserved **explicitly**, not by silence: accept
  `{ name = "test_foo", pending = "being written" }`, which registers as a `Kit.skip` rather than as
  nothing.
- `Kit.assertSuiteInventory(dir, suites)` globs `<dir>/test_*.lua` via the same `io.popen` `ls -A` /
  `dir /b` pair `vendor_sync` already carries (so no LuaFileSystem dependency appears) and fails on
  either asymmetry, with **two differently-worded messages** because the fixes differ: declared-but-missing
  says "delete the entry or write the file"; on-disk-but-undeclared says "add it to `tests/run.lua` — it
  is running zero cases today."
- Called automatically from `Kit.run` when `opts.dir` is given, with `opts.suiteInventory = false` as the
  documented opt-out for a repo mid-migration.

**Findings unblocked:** `AT-R-05`, `LK-R-01`, `LK-A-09`, `LH-A-29`, `CM-A-03`.

**Adoption cost downstream — this one is deliberately not additive.** It converts silence into failure.
Every kit consumer must be clean on adoption or its run reddens.

**Re-measured, because an earlier draft budgeted three hours for what is one `grep`.** Suites on disk
versus suites declared, today: AbsorbTracker **21/21**, BankLedger **20/20**, LootHistory **19/19**,
PanelMaster **20/20**, prettychat **16/16**, WhatGroup **14/14**. Every kit consumer is in balance and
adopts for free. More to the point, two of the three repos previously flagged as "a form the count could
not resolve" are the two that **already ship this exact gate**, and they are the reference implementations
the kit API should match:

- **BankLedger** — `tests/run.lua:17` says it outright ("tests/test_harness.lua asserts this list against
  tests/test_*.lua on disk, in both directions"); implementation at `tests/test_harness.lua:22-32`
  (`io.popen('ls tests/test_*.lua')`).
- **PanelMaster** — `tests/run.lua:60-63`; `tests/test_harness.lua:19-24` parses `local SUITES = {` out of
  the runner and `:28-32` globs the directory.
- **LootHistory** — 19/19 balanced but **ungated**; it gains the assertion here.
- **ConsumableMaster** — has no declared list at all: `tests/run.lua:26-32` auto-discovers via
  `io.popen("ls … /tests/test_*.lua")`, so it sits outside this assertion's premise entirely and is
  blocked behind `M3-10` regardless.

LibKa0s adopts first by construction (`M1-LK-11`). `M3-01` carries the pre-flight command that re-runs this
measurement per repo immediately before the copy, so a drift between now and adoption is caught rather than
assumed away.

**Effort:** M · **Risk:** medium.

---

## M1-LK-05 · `Kit.assertSurfaceParity(live, degraded, label)`

**File / symbol:** `testkit/framework.lua` — new assertion, exported through `Kit.expose`.

**Verified problem.** Three of the eight surviving Highs are one omitted stub member.
`PanelMaster/settings/Slash.lua` returns at `:316` without assigning `FormatKV`, so `/pm panel` raises on
exactly the degraded path the stub exists to survive. `ConsumableMaster/settings/Panel.lua:571-572` binds
`Helpers.RefreshAllPanels = UI and UI.RefreshAllPanels` and calls both bare at `:643` and `:833`.
`LootHistory/settings/Slash.lua:210` exports `HelpHeader` live and its degraded block at `:129-163` does
not. LootHistory is the only repo that tests this at all, and its case
(`tests/test_libka0s.lua:90-102`) enumerates members one assertion at a time — which is exactly why it
catches `SafeToString` and misses `HelpHeader`.

**Change.** Walk `live`'s keys; fail on any key absent from `degraded`, and on any key whose `type()` is
`function` live and not a function degraded (the ConsumableMaster shape — the key is present and
nil-valued, which a bare key check waves through). **Report every divergence in one message, not the
first**, because a stub written from a stale surface is typically wrong in several places and
one-at-a-time is three test runs. Accept an `ignore` set so a repo can encode "this member is live-only,
on purpose" as data rather than as an omission indistinguishable from a bug.

**Findings unblocked:** `PM-R-01`, `CM-R-01`, `CM-R-02`, `CM-A-25`, `LH-R-06`, `LH-A-39` — and the class
generally.

**Adoption cost downstream.** Additive. Each repo then writes one case per adopted seam (Core, Slash,
Options, DebugLog) — roughly four calls, an afternoon — and it reddens immediately in PanelMaster,
ConsumableMaster and LootHistory, which is the finding. The other five pay the same cost with an unknown
result.

**Honest limits, both worth stating so nobody over-claims.** It cannot catch a stub with the right member
set and a **wrong implementation**, so `KCD-A-14` (DebugLog stub re-implementing the library's line
format) and `PM-R-03` (hand-copied ack string) are **not** closed by it — those stay addon-side
`debug-logging-§7` violations. And it needs both halves loadable in one process, which ConsumableMaster
and KickCD only have because their private loaders provide it.

**Effort:** S · **Risk:** low.

---

## M1-LK-06 · Runner: executable at the source, and durations that cannot be negative

**File / symbol:** `testkit/run-automated-tests.sh` (timing at **`:86`**, `:126, :143, :148, :182, :187, :211, :216, :256, :272, :302, :313`);
git index mode of both `testkit/run-automated-tests.sh` and `tests/_kit/run-automated-tests.sh`;
new case in `tests/test_kitsync.lua`.

**Verified problem, both halves re-confirmed.**

1. `git ls-files -s` reports **`100644`** for `LibKa0s/testkit/run-automated-tests.sh` — the source every
   consumer copies from — and for all eight addons' `tests/_kit/run-automated-tests.sh`. That is 9/9.
   `automated-tests-§2` papers over it with a manual `chmod +x` step (`automated-tests.md:69`) that four
   of four adopters have missed, which is evidence about the step. It is inert here twice over: every one
   of the nine repos has `core.fileMode=false`, and this tree is DrvFs where every file reports
   `rwxrwxrwx`.
2. Every suite is timed with `t0=$(date +%s)` and reported as `$(( DUR * 1000 ))`: whole seconds, never
   clamped. A sub-second suite records 0; a clock that ticks backwards records a negative.
   `prettychat/docs/automated-tests/20260804-233338/manifest.json:16` carries `"durationMs": -1000`;
   `-2000` appears in AbsorbTracker's and BankLedger's manifests, `-1000` in KickCD's and LootHistory's.

**Change.**
- `git update-index --chmod=+x testkit/run-automated-tests.sh` in this repo, and the same for
  `tests/_kit/run-automated-tests.sh`.
- Add a case to `tests/test_kitsync.lua` asserting `git ls-files -s` reports **`100755`** for both paths.
  The **index mode, never `ls -l`** — this tree is DrvFs and reports `rwxrwxrwx` for everything, which is
  the trap `PM-A-11` and `CM-A-29` both had to explain. That gate is what stops the bit being lost on the
  next re-vendor.
- Resolve a millisecond source once at the top and reuse it: prefer `date +%s%3N`, fall back to
  `$EPOCHREALTIME`, fall back to seconds × 1000. Clamp every emitted duration with
  `[ "$d" -lt 0 ] && d=0`. Record which source was used in the manifest beside the tool versions, so a
  run with second-granularity timings is self-describing instead of looking like a fast run.
- **`:86` is in the list and is the one that must not be missed.** `RUN_START=$(date +%s)` at `:86` is the
  other operand of `:272`'s `RUN_DURATION=$(( $(date +%s) - RUN_START ))`, which `:313` multiplies by 1000
  into the run-level `durationMs`. Convert `:272` to milliseconds while leaving `:86` in seconds and the
  subtraction becomes epoch-milliseconds minus epoch-seconds — roughly 1.7 × 10¹² — written into every
  future manifest, **and the "no negative `durationMs`" check passes on it**. Convert both, or neither.

**Findings closed here:** `PC-R-07`. **Unblocked downstream:** `AT-A-05`, `BL-A-13`, `CM-A-29`, `PM-A-11`
(C18) — and the five unfiled repos.

**Adoption cost downstream.** Nine repos re-vendor. **The exec bit does not travel with `cp` or with the
file's bytes**, so each consumer still runs `git update-index --chmod=+x tests/_kit/run-automated-tests.sh`
once — the difference is that after this the kitsync case fails loudly if they forget, instead of the
omission surviving three audit cycles. Committed manifests keep their bad numbers: they are frozen
bundles and MUST NOT be rewritten.

Once the source is `100755` and gated, `automated-tests-§2`'s manual `chmod +x` step is redundant and is
retired by `M1-STD-06`.

**Effort:** S · **Risk:** low.

---

## M1-LK-07 · Runner: name the checkpoint; stop hardcoding `gating`

**File / symbol:** `testkit/run-automated-tests.sh:372` (the `RESULTS.md` lead-in printf) and `:322-323`
(the `gating` fields in `suite_json`).

**Verified problem.** Line 372 emits, into every repo's `RESULTS.md`:

> `**\`lint\` and \`tests\` gate. \`perf\` and \`complexity\` are recorded and never fail a run** —`

That sentence is true about a **run** and names no checkpoint, so the collection's docs collectively read
as "these two never gate anything", which `automated-tests-§3`'s release gate contradicts. Nine of nine
repos were written up for it (C8) and none of them wrote the sentence. Lines 322-323 hardcode
`"gating": false` for `perf` and `complexity`.

**Correction to the input analysis, verified.** The claim that the hardcoded `gating: false` makes the
release gate structurally unable to fire is **false**. `wow-addon/commands/bump-version.md:45-54`
evaluates the gate from `suites.<name>.status` and `suites.complexity.warnings`; it never reads `gating`.
The field is decorative. This item therefore fixes a **documentation defect in generated text**, and
optionally makes `gating` honest — it does not repair a broken gate.

**Change.**
- Rewrite the `:372` lead-in to name the checkpoint per suite: `lint` and `tests` gate the run and the
  commit; `perf` and `complexity` never fail a run or block a commit; the **tag** is gated on all four
  suites at `pass` plus zero functions above CCN 15 (`automated-tests-§3`), evaluated by
  `/wow-addon:bump-version` from this `manifest.json`, where a `skip` is NOT EVALUATED rather than a pass.
- Make `gating` describe the checkpoint rather than a boolean: emit
  `"gates": { "commit": false, "release": true }` for `perf` and `complexity`, and
  `{ "commit": true, "release": true }` for `lint` and `tests`. Keep the legacy `"gating"` boolean beside
  it for one revision so no reader breaks, and note in `docs/record-schema.md` that `bump-version` reads
  `status` and `warnings`, never these fields.

**Findings unblocked:** C8 in full — `AT-A-07`, `BL-A-12`, `CM-A-28`, `KCD-A-13`, `LH-A-36`, `PM-A-13`,
`PC-A-13`, `WG-A-14`, `LK-A-08` (9). This is the highest-leverage single edit in the collection: one file,
nine repos, nine findings.

**Adoption cost downstream.** Nine repos re-vendor and the next run rewrites the lead-in for them. The
hand-written half (`docs/testing.md`'s Gates? table, `docs/automated-tests/README.md`, two `CLAUDE.md`
sentences) is `M3-06`, driven by `M1-WA-02`. **Fixing this by hand-editing nine addons' docs is wrong** —
the next run regenerates the drift.

**Effort:** S · **Risk:** low.

---

## M1-LK-08 · `Perf`: observed containment, a cleared context, an honest docstring

**File / symbol:** `LibKa0s/Perf.lua` — `P.BUCKET_WITHIN` (`:348`), the bucket table print (`:214`),
`BuildRecord` (`:561`, `:574`), `addNestingNote`, `P.Open` (`:400-403`), `P.Close` (`:407-410`),
`P.Note` (`:367-376`), `P.Cancel` (`:822-840`), `P.context` (`:756`), `FormatReport` (`:919`), the
docstring at `:378-379`. New: `docs/api/Perf/version-N-docs.md`; new case in `tests/test_perf_isolation.lua`.

**Verified problem — three places where a capture record asserts something Perf does not know.**

1. **`within` is a pure declaration.** `Perf.lua:348` stores `P.BUCKET_WITHIN[b.key] = b.within` from the
   descriptor and nothing ever checks it, yet `:214` uses it to indent the bucket table, `:561` writes it
   into every saved record, and `addNestingNote` prints a containment sentence from it.
   `AbsorbTracker/core/PerfSetup.lua:46-47` declares `appearance` and `visibility` nested inside
   `repaintPass`; neither ever runs there, so every capture — including
   `docs/perf-runs/2026-07-30-ingame-post-extraction.json` — carries a false containment note. **Both
   bundles' proposed local fixes were themselves wrong**, because nobody could see the real nesting.
2. **`P.Cancel` leaves a stale stamp.** `:822-840` clears run/armed/recording/label and calls `P.Reset`,
   and never touches `P.context`, stamped at `:756`. A `perf report` after a cancel prints empty buckets
   wearing the discarded run's character, realm and zone.
3. **The docstring contradicts the standard.** `:378-379` says a call site "pays one boolean test and
   nothing else, and allocates nothing on either path". The off path is two real Lua calls, and
   `performance-§2`'s idiom is `local t0 = Perf.on and debugprofilestop()` — no call at all.

**Change.**
- **Make containment observed, not declared — against the bracket idiom that is actually in use.** An
  earlier draft specified this as "`P.Open` pushes a stack slot while `P.on`; `P.Close` pops and records
  `observedWithin[key][parentKey]`". **That mechanism can observe nothing, and it was checked.** Grepping
  all three wired addons returns **zero** `P.Open` / `P.Close` call sites: AbsorbTracker
  (`core/AbsorbTracker.lua:184`, `modules/Timer.lua:41`, `modules/Display.lua:105`, `:165`, `:202`),
  KickCD (`modules/Castbar.lua:716`, `modules/Cooldowns.lua:193`, `:201`, `:447`,
  `modules/IconGrid.lua:816`, `:935`, `:949`, `modules/IconGrid_Render.lua:746`, `:843`) and
  ConsumableMaster all use the inline idiom `local t0 = Perf.on and debugprofilestop()` …
  `Perf.Note(key, debugprofilestop() - t0)`. Independently, `P.Open()` (`LibKa0s/Perf.lua:400-403`) takes
  **no key** — the key arrives only at `P.Close(t0, key)` — so even a hypothetical `Open`/`Close` user
  leaves the stack slot without an identity while a child bracket is open, and `parentKey` is unknowable.

  **The shape that works with the deployed idiom:** take the parent explicitly at the recording call —
  `P.Note(key, ms, parentKey)`, defaulting to the declared `P.BUCKET_WITHIN[key]` when omitted, so every
  existing call site keeps working unchanged. `BuildRecord` emits declared **and** supplied, and
  `addNestingNote` refuses a containment sentence where the two disagree or the parent was never supplied,
  saying instead that the descriptor claims it and the capture did not see it. If the `Open`/`Close` pair
  is kept at all, change its signature to `P.Open(key)` so the slot has an identity; the additive
  alternative is a new `P.Enter(key)` returning `t0` with `P.Note(key, ms)` popping, which would change the
  **opening** line at every bracket site in AbsorbTracker, ConsumableMaster and KickCD — that cost belongs
  in the adoption paragraph, not hidden.

  **The unbalanced-bracket claim is withdrawn.** An earlier draft asserted that stack bookkeeping surfaces
  `KCD-R-05`/`KCD-A-18`'s two leaked exits "for free". It does not: those exits are `Note`-shaped, not
  `Open`/`Close`-shaped, so there is no open slot to leave dangling. Those two findings are closed by
  `M3-12`'s hand edit to `modules/IconGrid_Render.lua:831-837` and `modules/Castbar.lua:694-697`, and by
  `M3-12`'s per-bucket reachability case, not by this item.
- **Clear `P.context` in `P.Cancel`**, next to `P.label = nil` at `:838`.
- **Rewrite the docstring** at `:378-379` to state the real cost — two function calls plus the test,
  versus `performance-§2`'s inline form which is none — and say plainly when to prefer which, since the
  pair's whole justification is multi-exit ergonomics. Pairs with `M1-STD-14`.
- Guard `P.Note` against a nil key so `P.Close` with a typo'd key fails at the call site with a framed
  message rather than "table index is nil" (`LK-R-05`).

**Findings closed here:** `LK-R-04`, `LK-R-05`, `LK-R-06`. **Unblocked downstream:** `AT-R-01`,
`KCD-R-05`, `KCD-A-18`, `CM-A-07`, `CM-A-08`, `CM-A-13`.

**Adoption cost downstream — stated honestly, because the earlier "no addon must do anything" line is what
concealed the defect above.** Descriptors are unchanged and `P.Note(key, ms)` keeps its old meaning, so
nothing breaks on adoption. But observed containment is only reported for buckets whose call site **passes
the parent**, so the value AbsorbTracker needs from this item arrives only after `M3-12` adds the third
argument at `modules/Display.lua:105` and `:165`. That is two edited lines in one repo, and it is the
whole reason `M3-12` depends on this item rather than merely following it. ConsumableMaster and KickCD may
adopt the third argument or not; without it they get the declared value and an explicit "not observed"
note, which is still an improvement on today's silent false claim.

**Risk note.** This is the one Milestone-1 item that touches shipped in-game code. The stack must be
provably free when `P.on` is false, and that claim needs a case in `tests/test_perf_isolation.lua` —
which is the zero-overhead scenario `performance-§2` requires and which the library does not currently
hold for itself. Bump the `Perf` minor and write the API document; `tests/test_versioning.lua` enforces
the pairing.

**Effort:** M · **Risk:** medium.

---

## M1-LK-09 · `Options`: publish the layout constants hosts are provably re-typing

**File / symbol:** `LibKa0s/Options.lua:176-178` (the instance publish block), `lib.LAYOUT` (`:44-77`);
new case in `tests/test_options.lua`; new API document.

**Verified problem.** `lib.LAYOUT` holds thirteen constants; the instance publishes three — `ROW_VSPACER`,
`SECTION_HEADING_H`, `BUTTON_PAIR_REL` (`:176-178`). `PADDING_X` (defined `:46`) is used at seven sites
inside the library — `:193, :202, :203, :303, :331` (comment), `:333, :334` — and is not among them, so a
host that needs to align a bespoke widget with the library's header and divider has no way to read it.
KickCD restates it as `core/Constants.lua:66 Const.PANEL_PADDING_X = 16` and reads it at
`settings/Panel.lua:307`. `options-ui-§8`'s MUST NOT against host copies **cannot be complied with** for a
constant the library keeps to itself.

**Change — one scalar, not six.** Publish **`PADDING_X`** on the instance. **As an individual scalar,
deliberately not as `O.LAYOUT = L`** — handing out the lib-level table lets one host's mutation retune every
other host's panels, which is a worse failure than the copying this fixes. Add a case pinning that every key
of `lib.LAYOUT` is either published on the instance or carries an in-file comment saying why it is internal,
so the next constant added does not recreate the gap.

**Why the other five stay internal.** An earlier draft also published `HEADER_TOP`, `HEADER_HEIGHT`,
`DEFAULTS_W`, `SECTION_TOP_SPACER` and `SECTION_BOTTOM_SPACER`. **None of the five has a demonstrated
consumer anywhere in the collection** — the only host copy in evidence is KickCD's `PANEL_PADDING_X`
(`KCD-A-03`), and this item's other driver, `CM-A-05`, is already fixable today because
`SECTION_HEADING_H` and `BUTTON_PAIR_REL` are published. Publishing five scalars on frequency rather than
on a demonstrated need is anti-pattern **#55** verbatim — *"promoting a shape into a shared lib because it
is repeated, rather than because it is shared … under the additive-only rule a wrong shared abstraction is
surface the library keeps forever"* — added to the standard at v2.21.0, one day before this plan
(`library-stack-§7`). Each of the five is published the day a host demonstrates it needs it; the new
`tests/test_options.lua` case is what keeps that decision visible rather than forgotten.

**Findings unblocked:** `KCD-A-03` (unfixable downstream today). `CM-A-05` is **not** unblocked by this
item — it is already fixable against the three constants published today, and `M3-13`'s ConsumableMaster
half does exactly that.

**Adoption cost downstream.** Additive; no consumer changes behavior. KickCD deletes
`core/Constants.lua:66` and reads `O.PADDING_X` at `settings/Panel.lua:307`, and drops
`local ROW_VSPACER = 8` at `settings/Panel.lua:426`, which currently overwrites the published
`O.ROW_VSPACER` at `:430`. Values are unchanged, so **no panel moves a pixel**.

**Effort:** S · **Risk:** low.

---

## M1-LK-10 · US-English sweep of authored comments in `LibKa0s/` and `testkit/`

**File / symbol:** `LibKa0s/Core.lua` (`:76-79, :100, :156, :257`), `LibKa0s/DebugLog.lua`
(`:180, :216, :230, :304`), `LibKa0s/Options.lua:525`, `LibKa0s/OptionsWidgets.lua` (`:32, :56`),
`LibKa0s/Perf.lua`, `LibKa0s/Slash.lua`, `testkit/README.md`, `testkit/run-automated-tests.sh:117`
("Strip ANSI colour" — the earlier draft cited `:118`, which is the following line). New guard case in `tests/test_kitsync.lua` or a new `tests/test_prose.lua`.

**Verified problem.** 33 hits for `colour`/`grey`/`behaviour`/`synthesis`/`normalis`/`recognis` across
the shipped library files; `Core.lua:76-79` alone carries four in one paragraph. `localization-§5`
mandates US English and anti-pattern #46 names code comments explicitly. This surfaces in consumers as a
finding against *them* — WhatGroup's review counts 29 hits under its own `libs/LibKa0s/` (`WG-R-09`) —
and **no consumer can fix it**: a local patch is reverted by the next whole-folder re-vendor
(anti-pattern #48).

**Change.** Sweep comments and docstrings only. Do not touch `lib.SKIN` keys, any identifier, or any
user-visible string — there are none in the hit set, which is why this is zero-risk. Two carve-outs into
the commit message so a future sweep does not undo them: Blizzard symbols reproduced verbatim
(`SetColorTexture`, `SetBackdropBorderColor`) stay, and released `CHANGELOG.md` entries are history and
stay. Add a guard case grepping the shipped files for the anti-pattern #46 word list and failing with the
`file:line` list. **The guard is the part with lasting value**; the sweep alone regresses on the next
feature.

**This item also carries LibKa0s's shipped-source `§N.M` sweep** — `LibKa0s/LibKa0s/Options.lua:129` and
`:173`, both reading "Ka0s standard §3.4". They belong here, not in `M3-07`, because `Options.lua` is
vendored byte-for-byte into all eight addons; changing it after `M3-01`'s re-vendor would redden eight
consumers' `tests/test_vendor_sync.lua` against a payload they cannot patch (invariant 3), with no second
re-vendor scheduled. Folding them into this commit means one release carries both prose sweeps.

**The guard's grep must be written as a real ERE — and copied as one.** In `04_EXECUTION_PLAN.md`'s tables
the pattern appears as `colour\|grey\|behaviour`, where `\|` is **GFM table escaping**: it renders as a
literal pipe, so the *rendered* command is a correct alternation. Copy it out of the **raw markdown**
instead and you get a test that cannot fail — under `-E`, a real `\|` matches a literal pipe character, so
the pattern becomes the single string `colour|grey|behaviour`, which appears nowhere. Verified against a
file containing both "colour" and "behaviour": the backslash form exits 1 with no output; the plain ERE
matches both. Write the guard case as
`grep -rniE "colour|grey|behaviour|synthesise|normalis|recognis" LibKa0s/ testkit/` with no backslashes,
and — per this document's standing rule — show it **red against a deliberately planted violation** before
accepting it.

**Findings closed here:** `LK-A-06`. **Unblocked downstream:** `WG-R-09` (closes on WhatGroup's next
re-vendor with no work of its own), and `KCD-A-16` in part — KickCD's remaining hits are in its own plan
document.

**Adoption cost downstream.** Bytes change in every shipped library file, so every consumer's
`tests/test_vendor_sync.lua` demands a re-vendor to the tag carrying it — which is only true once they
bump their README provenance line, so no consumer is forced to move on this repo's schedule. Zero
behavioral change, zero API change; **fold it into whichever release carries `M1-LK-08` or `M1-LK-09`**
rather than cutting a release for prose.

**Effort:** M · **Risk:** low.

---

## M1-LK-11 · LibKa0s's own runner adopts the derivation and the inventory

**File / symbol:** `LibKa0s/tests/run.lua:17-19` (library file list) and `:76-80` (suite list).

**Verified problem.** Both lists are hand-written; `LibKa0s/LibKa0s.xml:2-9` is never parsed by any test;
`testkit/framework.lua:101-110` silently skips a missing suite. The only mitigation
(`tests/test_versioning.lua:43-57`) catches a file already declared in MAJORS. `testing-§10` names this
repo as the reference implementation for exactly this family of gates.

**Change.** `:17-19` becomes `Loader.xmlFiles("LibKa0s/LibKa0s.xml")` (`M1-LK-03`). `:76-80` stays a
declared list but is now pinned in both directions by `Kit.assertSuiteInventory` (`M1-LK-04`).

**Findings closed here:** `LK-R-01`, `LK-A-09`.

**Adoption cost downstream.** None. This is the reference implementation catching up with what it asks of
everyone else, and the addons copy the shape in `M3-03`.

**Dependencies:** `M1-LK-03`, `M1-LK-04`. **Effort:** M · **Risk:** low.

---

## M1-LK-12 · LibKa0s documentation and test corrections

**File / symbol:**
- `docs/releasing.md:146` — the false claim that `tests/test_versioning.lua` gates API documents; it
  checks `CHANGELOG.md` only (`:107-128`) and `tests/test_kitsync.lua:81-94` is the sole API-document
  gate, covering the kit alone. Either implement the gate or delete the sentence.
- `docs/releasing.md:28-59` — the numbered release order contains no `run-automated-tests.sh` step, so
  the only bundle is `20260805-002859` at `"release": null` with `"dirty": true`, on a commit later than
  `v1.7.0^{}` (`6ce8548`). Add the step.
- `tests/test_perf_core.lua:15-24` — four bare `assertFalse` with no message check; the `name` arm is
  unfalsifiable because `LibKa0s/Perf.lua:328` raises independently of the `:290` guard. Assert on the
  message, as the adjacent case at `:26-41` already does.
- `README.md:196-231` — `## Repo layout` omits `docs/automated-tests/` and `docs/audits/`, both on disk.
- `docs/automated-tests/README.md:27-36` — the hand-written half of the release-gate omission; the
  `RESULTS.md` half is runner-emitted and fixed by `M1-LK-07`.

**Findings closed here:** `LK-R-02`, `LK-A-15`, `LK-R-03`, `LK-A-10`, `LK-A-07`, `LK-A-11`, `LK-A-08`.

**Adoption cost downstream.** None. **Effort:** S · **Risk:** low.

---

## M1-LK-13 · LibKa0s adopts the library-repo documentation set

**File / symbol:** new root `CLAUDE.md` carrying `## Standards compliance (read first)`; new root
`DEPENDENCIES.md`; `README.md` standards reference.

**Verified problem.** Every rule in `documentation` opens "Every Ka0s addon", and LibKa0s is not in
`standards/ADDONS.md:19-26`. Six findings (C13) are addon-shaped rules applied to a repo with no TOC and
no player-facing README. The audit's own `01_CURRENT_STATE` claims it carved out addon-only rules and
then audited the addon-scoped documentation section anyway.

**Change — after `M1-STD-07` defines what actually binds a library repo.** Write the three documents
that section will name: a root `CLAUDE.md` whose only mandated content is the compliance section (the
one of `documentation-§6`'s three places that exists in a repo with no TOC and no player README); a root
`DEPENDENCIES.md` recording the toolchain (`lua5.1` with `setfenv`, `luacheck 1.2.0`, `lizard 1.23.0` —
read from `docs/automated-tests/20260805-002859/manifest.json`); and a README pointer to the standard,
which currently appears only in `CHANGELOG.md:418`, `:475` and `docs/automated-tests/README.md:4`.

**Findings closed here:** `LK-A-01`, `LK-A-02`, `LK-A-03`, `LK-A-04`, `LK-A-05`, `LK-A-12` — with
`LK-A-04` and `LK-A-05` resolved by `M1-STD-07` declaring the `docs/` trio addon-scoped, since the content
already exists at `README.md:121-159` and `:196-231`.

**Adoption cost downstream.** None; no addon repo changes.

**Dependencies:** `M1-STD-07`. **Effort:** M · **Risk:** low.

---

## M1-LK-14 · Cut the LibKa0s release — the item every M3 adoption depends on

**File / symbol:** `docs/releasing.md` steps 1–7, executed. `testkit/framework.lua` (`Kit.VERSION`), the
`MINOR` / `WIDGETS_MINOR` / `SCROLL_MINOR` / `PANEL_MINOR` constant of every file `M1-LK-08`, `M1-LK-09`
and `M1-LK-10` touched, `CHANGELOG.md`, `docs/api/<Major>/version-<minors>-docs.md`, `docs/test-cases.md`,
the provenance template in `docs/releasing.md`, the repo semver, the tag.

**Verified problem.** Every Milestone-3 adoption item is written against "the LibKa0s tag carrying kit
revision 8", and **no work item cuts that tag.** `M1-LK-01` … `M1-LK-13` contain no version bump, no
`CHANGELOG.md` block, no API document beyond the two their own items name, and no tag; Milestone 1's exit
criteria never mention one. The latest tag today is **v1.7.0** (`git -C LibKa0s tag | tail -1`). Without
this item `M3-01` cannot start, and `M1-LK-01`'s own verification — "`lua5.1 tests/test_kitsync.lua` green
after re-vendor" — silently assumes a step that is not scheduled.

`docs/releasing.md:20-59` makes this a gated procedure the rest of the plan partially contradicts:

- **Step 2** requires bumping the named minor constant of **every** file changed, by its exact constant
  name — `MINOR` in `Core.lua`, `DebugLog.lua`, `Slash.lua`, `Options.lua` and `Perf.lua`,
  `WIDGETS_MINOR` in `OptionsWidgets.lua`, `SCROLL_MINOR` in `OptionsScroll.lua`, `PANEL_MINOR` in
  `PerfPanel.lua` — plus `Kit.VERSION` if `testkit/` moved, and a re-vendor into this repo's own
  `tests/_kit/`. `M1-LK-10` alone touches `Core.lua`, `DebugLog.lua`, `Options.lua`, `OptionsWidgets.lua`,
  `Perf.lua` and `Slash.lua`; the individual items bump only the `Perf` and `Options` minors.
- **Step 3** — a new module is also a new row in `tests/run.lua`'s `MAJORS`. Nothing here adds a module,
  so this step is a no-op; record it as checked rather than skipped.
- **Step 4** requires a `CHANGELOG.md` version block; `tests/test_versioning.lua` fails when it and
  `lib.MODULES` disagree.
- **Step 5** requires an API document per moved minor, plus the superseded document's `Status` /
  `Superseded by` edit and a row in `docs/api/README.md`.
- **Step 6** regenerates `docs/test-cases.md` (`lua tests/run.lua --list`, keeping CRLF).
- **Step 7** moves the provenance template and the repo semver to the version being released, **before**
  the tag, so the tagged commit already states what it bundles.

**Change.** Execute steps 1–7 verbatim, once, for **v1.8.0**, after `M1-LK-01` … `M1-LK-13` (and
`M1-LK-15` if `M1-STD-11` picks option (b)) are all in.

**Verified by.** `git tag --points-at HEAD` → `v1.8.0`. `lua5.1 tests/test_versioning.lua` green.
`lua5.1 tests/run.lua` green. `git ls-files -s testkit/run-automated-tests.sh` → `100755`.
`diff` of `lua5.1 tests/run.lua --list` against `docs/test-cases.md` empty after CR-normalizing both sides.

**Adoption cost downstream.** This is the item `M3-01` depends on, and the reason `M3-01`'s dependency
column names `M1-LK-14` rather than `M1-LK-01…07`.

**Dependencies:** `M1-LK-01` … `M1-LK-13`, and `M1-LK-15` under `M1-STD-11` option (b).
**Effort:** M · **Risk:** medium.

---

## M1-LK-15 · **CONDITIONAL** — a varargs printer on the `Core.lua` seam

**Scheduled only if `M1-STD-11` resolves `events-frames-taint-§8` as option (b).** Under option (a) this
item does not exist and Milestone 1 has 41 items; under option (b) it exists and Milestone 1 has 42.

**File / symbol:** `LibKa0s/Core.lua`'s printer seam — add `NS.Print(fmt, ...)` accepting a format string
plus varargs and doing the formatting inside the library, so the compliant call is no longer than the
`("…"):format(…)` bypass it replaces. Minor bump on `Core.lua`, API document,
`tests/test_versioning.lua` pairing, and inclusion in `M1-LK-14`'s release.

**Why it must be here and not in M3.** `M1-STD-11` option (b) is "require a varargs printer from LibKa0s
and keep the MUST unscoped". That is a **LibKa0s API addition**, and this plan's one hard rule is that
every upstream change is in Milestone 1. Without this item, `M4-27` schedules AbsorbTracker's 18 sites,
PanelMaster's ~25, KickCD's `modules/Castbar_Debug.lua` and WhatGroup's two `pout` arms against a library
API that has no item, no release and no vendoring step.

**Adoption cost downstream.** Every one of those ~50 call sites is mechanically rewritten in `M4-27`, and
`M4-27` then additionally depends on `M3-01`'s library-half re-vendor before a single one can be converted.
Under option (a) the same `M4-27` is a re-grade and a register row — the two branches differ by roughly two
orders of magnitude, which is why the fork is flagged in `00_OVERVIEW.md` and `05_TRACEABILITY.md` rather
than absorbed into a single headline number.

**Dependencies:** `M1-STD-11` choosing (b). Folds into `M1-LK-14`. **Effort:** M · **Risk:** low.

---

# Group B — WowAddonStandards

Path: `/mnt/d/Profile/Users/Tushar/Documents/GIT/WowAddonStandards`
Current version **v2.21.0 (2026-08-04)**. Target **v2.22.0**.

**Append-only discipline.** Where a new subsection is added to a file that already has numbered
subsections, it is **appended**, never inserted, so no existing `filename-§N` reference renumbers. This
is the discipline v1.11.0 used for `debug-logging-§8`/`§9`/`§10`.

---

## M1-STD-01 · `performance-§12` — the no-combat-path exemption

**File / section:** `standards/standards/performance.md`, new `### 12. When the wiring does not apply —
the no-combat-path exemption (MUST qualify, MUST record)`. Verified: `performance.md` currently carries
§1–§11, so §12 is the correct append.

**Verified problem.** `performance.md`'s *Adoption strength* makes the wiring an unconditional MUST
(vendor, instance at load, `perf` verb, `<Addon>PerfDB`, suspend/resume). Five of the eight roster addons
declined it independently on the same structural ground, recorded in their own `docs/pending/LEDGER.md`:
the harness opens a window only when `UnitAffectingCombat("player")`, and these addons run no code there —
so every bucket reads 0.000 by construction, which `performance-§3` itself calls a lie, and `suspend`
would drop the very data the addon exists to record. Because the MUST is unconditional, each audit
re-files the whole cascade as independent High MUST failures: **32 rows across five repos**, every one
marked derivative by triage, several of which would make the addon *worse* if acted on (declaring
`<Addon>PerfDB` that nothing writes; a `perf` verb dispatching into an instance that does not exist).

**Change.**

1. **The qualifying test.** Criterion (a) MUST hold: no `OnUpdate` handler, no repeating ticker, and no
   event handler doing more than occasional work while the player is in combat — proven by a committed
   whole-repo sweep of `RegisterEvent` / `SetScript("OnUpdate"` / `C_Timer` naming the per-event work.
   The record MUST also name whichever of (b) "the two arms cannot differ — every declared bucket would
   read 0.000 by construction" or (c) "suspend would suppress the data the addon exists to record"
   applies.
2. **What the exemption suspends:** `performance-§1`'s instance and setup file, `§4`'s verb registration,
   `§5`'s `<Addon>PerfDB`, `§6`'s suspend/resume contract, `§9`'s `tests/perf.lua`, and
   `documentation-§3`'s `docs/perf-runs/README.md`.
3. **What it does NOT suspend:** whole-folder vendoring of `libs/LibKa0s/` (anti-pattern #48); `perf`
   remaining a reserved verb meaning nothing else (`slash-commands-§2`); `docs/performance.md`, which
   stays required and shrinks to a one-screen page stating the addon brackets nothing and why; and
   `automated-tests-§3`'s `perf: skip` release-notes line.
4. **The re-check trigger.** The first `OnUpdate`, repeating ticker or in-combat event handler re-arms
   the full wiring MUST, and the register entry says so.
5. **Claimed once**, in the deviation register (`M1-STD-02`), never per audit.

**Ripple edits, all one or two lines each:** `performance.md`'s *Adoption strength* paragraph and §1's
first bullet gain the pointer; `toc-file.md` §2 bullet 2 becomes two-when-wired / one-when-exempt / never
three; `savedvariables.md` §4's opening paragraph; `slash-commands.md` §2 (reserved always, registered
when wired); `lint.md`'s `globals`/`read_globals` comments; `documentation.md` §3's required-five list
(`perf-runs/README.md` conditional, `performance.md` restated as required-but-short); `automated-tests.md`
§3's skip exception gains the exemption as a second sanctioned `skipReason`; `testing.md` §8's
per-adopted-module list; `EXECUTIVE_SUMMARY.md` pattern 6; `NEW_ADDON_CONTEXT.md` keeps wiring as the
scaffold default (a new addon has no sweep evidence yet) and gains one line pointing at `performance-§12`.

**Findings unblocked:** C1's 40, of which 32 close via `M3-09` and 7 become genuine residual work in the
two wired repos (`M4-25`).

**Adoption cost downstream.** AbsorbTracker, ConsumableMaster and KickCD: **no change** — harness wired,
still bound by the full section. BankLedger, LootHistory, PanelMaster, prettychat, WhatGroup: each
converts an existing LEDGER decline into one register entry carrying the sweep (S — the sweep is already
written in four of the five ledgers) plus a short `docs/performance.md` (S), and stops carrying six or
seven recurring MUST rows per audit. LootHistory additionally gets its standing `perf: skip`
release-notes obligation named rather than re-derived.

**Effort:** L · **Risk:** medium.

---

## M1-STD-02 · A fixed home and row shape for an accepted deviation

**File / section:** `standards/standards/documentation.md` §3 (add `## Documented deviations` as a ninth
mandated `docs/ARCHITECTURE.md` section); `standards/standards/audit-review-history.md` (two new MUSTs).

**Verified problem.** `documentation-§2` and `§6` both say "record it as a documented deviation" and name
no file — the closest is the parenthetical "e.g. in the TOC/README/`docs/` and in the audit bundle" at
`documentation.md:163-183`. Every repo invented its own home: BankLedger uses
`docs/ARCHITECTURE.md:568-581`, KickCD a register in the same file, ConsumableMaster `docs/scope.md:20`,
prettychat `CLAUDE.md:5-13` plus `docs/pending/LEDGER.md`, WhatGroup and LootHistory the ledger only.
Two failures follow. Audits cannot find a ratified decision and re-file it (`BL-A-01` carried in the MUST
column though recorded exactly where the process asks; `CM-A-01`, `WG-A-01`, `PC-A-02` likewise) —
conversely `BL-A-02`'s live gap is precisely the *missing* ARCHITECTURE entry for a decision that lives
only in the ledger. And a register nobody re-reads goes stale in the dangerous direction:
`AbsorbTracker/docs/ARCHITECTURE.md:277-315` lists four behaviors the standard now mandates or permits as
deviations, three marked "Pending promotion" for a rollout that already shipped.

**Change.**

1. `documentation.md` §3: add `## Documented deviations` to `docs/ARCHITECTURE.md`'s mandated section
   list — currently Overview, Module Map, Settings Schema, Message Bus, Slash Commands, Event
   Subscriptions, Taint Notes, Known Limitations — with a fixed row shape
   `| Rule | What differs | Why | Decided | Re-check trigger |`, where **Rule** is a `filename-§N`
   reference, **Decided** is a date, and **Re-check trigger** is the condition that ends the deviation
   (`performance-§12`'s exemption is the model). State that this is the **single home**: a decision may be
   *reasoned* in `docs/pending/LEDGER.md` or an audit bundle and the row cites that id, but a deviation
   not in the register is not ratified.
2. `audit-review-history.md`: an audit MUST read the register first and record a ratified entry as
   *accepted, with its id*, not as an open MUST failure; and MUST report as a finding any entry whose
   cited rule the standard has since changed, so the register cannot accumulate compliant behavior.

**Ripple:** `EXECUTIVE_SUMMARY.md`'s doc-set paragraph; the canonical CLAUDE.md wording block at
`documentation.md:163-183`; `NEW_ADDON_CONTEXT.md`'s ARCHITECTURE template.

**Findings unblocked:** C4's 13, plus `BL-A-01`, `BL-A-02`, `AT-A-09`, `LH-A-20`, `PM-A-01`.

**Adoption cost downstream.** All eight addons add one ARCHITECTURE section; for six it is a move of text
that already exists (S each). BankLedger and KickCD already have a register and only reshape rows.
AbsorbTracker additionally retires the four stale entries at `docs/ARCHITECTURE.md:277-315` (S). No code
changes anywhere.

**Effort:** M · **Risk:** low.

---

## M1-STD-03 · `testing-§11` — the consumer-side gate, and a case-level skip

**File / section:** `standards/standards/testing.md` §11 (scope widened), §5 (inventory and badge count
passes); `standards/standards/automated-tests.md` §4 (`RESULTS.md` tests column).

**Verified problem.** `testing-§11` specifies the byte-identity gate for the *library* repo's `testkit/`
against its own `tests/_kit/` and says nothing about the consumer side — yet seven repos ship a
consumer-side `tests/test_vendor_sync.lua`, all copied from each other and all broken the same way. The
honest fix is unavailable: `testkit/framework.lua` (`Kit.VERSION = 7`) has a registry and assertions and
**no case-level skip**, so the only expressible outcomes are pass and fail. `testing-§11`'s "MUST fail
when the gate cannot run" is unimplementable without making every fresh clone red — which is exactly why
every repo chose silence.

**Change.**

1. §11 covers both halves. Every repo vendoring a Ka0s-owned library MUST carry a gate comparing
   `libs/LibKa0s` against the sibling checkout's ship folder. When the precondition is absent the case
   MUST register as a **skip carrying its reason**, MUST NOT register as a pass, and the reason MUST be
   visible in the case's own recorded result rather than only in a header comment.
1b. **Scope the existing no-normalization MUST, which is where an earlier draft went wrong.**
   `testing.md:231-233`'s "MUST compare raw bytes … with no line-ending normalization" is written for a
   comparison where **both sides are the same representation** — the library repo's own `testkit/` against
   its own `tests/_kit/`, two working-tree directories in one checkout. §11 MUST say so, and MUST state
   the carve-out explicitly for the consumer-side gate, where one side is a **`git show` blob** (LF, by
   construction) and the other is a **working tree** pinned to CRLF by `.gitattributes` in eight of the
   nine repos. Measured: `git -C LibKa0s show HEAD:LibKa0s/Core.lua | tr -cd '\r' | wc -c` → **0**;
   `tr -cd '\r' < AbsorbTracker/libs/LibKa0s/Core.lua | wc -c` → **322**. There, **exactly one**
   normalization is permitted and required — CR stripped from the working-tree side, nothing else — or,
   equivalently and normalization-free, `git hash-object` on the local file compared against the blob sha.
   Without this carve-out the MUST reddens the gate in seven repos on the commit that adopts it, and
   `ConsumableMaster/tests/test_vendor_sync.lua:133`'s `gsub` — which an earlier draft ordered deleted —
   is the line that makes the comparison meaningful in the first place.
2. Name the primitive: `Kit.skip(reason)` (`M1-LK-01`), surfaced by `Kit.run` and the `--list` renderer,
   so a skip is a third status in `docs/test-cases.md` and in the runner's tests figures.
3. Amend §5: the inventory and the `[tests]` badge count **passes**, and a skipped case MUST be shown as
   skipped rather than folded into either number. Amend `automated-tests-§4`'s `RESULTS.md` row contract
   so the tests column carries passed/skipped/total.

This is the doctrine `automated-tests-§3` already applies to an absent tool — record a missing tool as a
skip with its reason, never as a pass or a failure — extended from suites to cases.

**Findings unblocked:** C6's 10.

**Adoption cost downstream.** LibKa0s carries the real work (`M1-LK-01`, `M1-LK-02`). Then eight addons
re-vendor, change two lines each, and regenerate `docs/test-cases.md`. Badge values are unchanged because
pass counts do not move. **Until the kit lands, addons cannot comply — sequence LibKa0s first.**

**Effort:** M · **Risk:** low.

---

## M1-STD-04 · `testing-§8` — stub-surface parity, and anti-pattern #56

**File / section:** `standards/standards/testing.md` §8 (new MUST after the degraded-path paragraph);
`standards/standards/anti-patterns.md` #56 (verified: the list currently ends at #55);
`STANDARDS.md` Sections blurb (`#1–#55` → `#1–#56`).

**Verified problem.** The most damaging defect class in the whole set is a degradation stub that omits a
member the host calls. `performance-§1` already names it in prose — "a stub that omits a member the slash
layer calls is not a fallback, it is a crash moved to a rarer code path" — and `AUDIT.md` asks a human
auditor to grep the call sites and check by hand. That human check is the only gate, and it misses:
`ConsumableMaster/settings/Panel.lua:571-572` and `:643`/`:833` (reproduced by execution as a session-long
error loop with a settings write landing before the raise); `PanelMaster/settings/Slash.lua:316` versus
five host-owned `FormatKV` call sites (also reproduced); `ConsumableMaster/settings/Slash.lua:341`
blacking out all 17 verbs including the 11 that never used the library, against `slash-commands-§1`'s "the
host verbs never went to the library, so they keep working". `testing-§8` lists "the degraded path" as one
of four minimum integration cases but asks only that the addon *loads*, which every one of these does.

**Change.**

- §8 gains a MUST: for each adopted LibKa0s module the addon MUST carry a **stub-surface parity case** —
  a declared list of the members the addon reaches on that instance (grep-derived, **with the grep named
  in the case comment** so the next author re-runs it rather than re-derives it), asserted present on
  both the live instance and the library-absent stub, with the degraded arm produced by feeding the
  loader a deliberately partial file list, **never** by hand-stubbing the namespace member under test
  (which §8 already forbids). State explicitly that the options stub's load-completing exception
  (`options-ui-§1`) narrows what the members must *do*, not which members must *exist* — that exception
  is what both ConsumableMaster failures hid behind.
- Anti-pattern **#56** — a degradation stub whose member set has drifted from the host's call sites, with
  the two reproduced failure shapes (a bare call on a nil member after the write already landed; a stub
  that refuses verbs that never went to the library) and the note that it is invisible to every green
  suite because no suite loads the addon degraded.

**Findings unblocked:** `CM-R-01`, `CM-R-02`, `CM-A-25`, `CM-A-32`, `PM-R-01`, `LH-R-06`, `LH-A-39`.

**Adoption cost downstream.** Eight addons add one case per adopted module — S in AbsorbTracker,
BankLedger, KickCD, prettychat, WhatGroup (stubs believed correct; the case pins them); M in
ConsumableMaster and PanelMaster, where the case is written red and fixes three reproduced defects; S in
LootHistory, extending an existing case. **No library change required** — the loader already supports
partial file lists — though `M1-LK-05` makes the case a one-liner instead of an enumeration.

**Effort:** M · **Risk:** low.

---

## M1-STD-05 · Every "never fail a run" statement MUST name its checkpoint

**File / section:** `standards/standards/automated-tests.md` §4 (a MUST on the runner's emitted lead-in);
`standards/standards/testing.md` §6 and `documentation.md` §3's `docs/testing.md` bullet (the gate table
carries the checkpoint per suite).

**Verified problem.** Nine repos were each written up as having the v2.21.0 release gate stated nowhere,
and every triage reached the same verdict: the repo's own sentences are true about runs, and **no section
obliges an addon to restate a gate the release command evaluates from `manifest.json`**. So the audits are
generating a finding per repo against a rule that does not exist, while the underlying complaint is real —
the docs collectively read as "these two never gate anything". The load-bearing detail is that one of the
two offending sentences is not authored per repo at all: `LibKa0s/testkit/run-automated-tests.sh:372`
generates it into every repo, so eight identical half-truths were emitted by the tool the standard
mandates, and no addon can fix its copy without forking a file `testing-§1` forbids editing.

**Change — deliberately small, and no new obligation to restate the release gate.**

1. `automated-tests-§4` gains a MUST on the **generated lead-in's content**: the text the runner writes
   into `RESULTS.md` MUST name the **checkpoint** for each suite, not merely the verdict — `lint` and
   `tests` gate the run and the commit; `perf` and `complexity` never fail a run or block a commit; the
   **tag** is gated on all four plus zero functions above CCN 15 (`automated-tests-§3`), and a `skip`
   there is NOT EVALUATED rather than a pass. Same register §4 already uses for `RESULTS.md`'s columns.
2. `testing-§6` and `documentation-§3`'s `docs/testing.md` bullet: the verify-how-to page's gate table
   MUST carry the checkpoint per suite (commit / release), so `Gates? no — recorded only` cannot stand
   unqualified.

**Findings unblocked:** C8's 9.

**Adoption cost downstream.** LibKa0s edits the printf block (`M1-LK-07`), bumps the kit, re-vendors.
Eight addons re-vendor and edit one table in `docs/testing.md`; ConsumableMaster and KickCD also fix one
`CLAUDE.md` line each. LibKa0s's own `docs/automated-tests/README.md` picks up the same wording. No code,
no test changes.

**Effort:** S · **Risk:** low.

---

## M1-STD-06 · `automated-tests-§2` — the exec bit that matters is the git index mode

**File / section:** `standards/standards/automated-tests.md:69` (replace the closing `chmod +x` sentence).

**Verified problem.** `automated-tests.md:69` closes its vendoring MUST with "re-vendoring ends with
`chmod +x tests/_kit/run-automated-tests.sh`". That instruction is wrong for the environment the
collection develops in, and it failed identically in **9/9 repos**: `git ls-files -s` reports `100644`
everywhere including LibKa0s's own two copies, while every working tree shows `rwxrwxrwx` because the
repos sit on a WSL DrvFs mount that reports every file executable — and every repo has
`core.fileMode=false`, so a `chmod` that did fire would be ignored by git anyway. Nine identical failures
against an explicit MUST is evidence the instruction is defective.

**Change.** Replace with the index-mode form —
`git update-index --chmod=+x tests/_kit/run-automated-tests.sh` — and state the trap plainly: the mode
that survives a clone is the one in the git index; on a DrvFs/WSL checkout the working tree reports every
file executable, so `ls -l` and a successful `chmod` are both silent about the real state. Add a MUST
that the repo's vendored-payload gate (`M1-STD-03`'s consumer-side gate, or `tests/test_kitsync.lua` for
LibKa0s) asserts the recorded mode is `100755`, so this is checked mechanically rather than remembered.

**Findings unblocked:** C18's 4 filed, plus the 5 unfiled repos.

**Adoption cost downstream.** Eight addons run one git command and commit (S each). One assertion added
per repo's vendor-sync suite, or once in LibKa0s's kit if the gate ships there (`M1-LK-06`).

**Effort:** S · **Risk:** low.

---

## M1-STD-07 · `library-stack-§7` + `ADDONS.md` — what binds a Ka0s-owned library repo

**File / section:** `standards/standards/library-stack.md` §7 (new *Applicability* block);
`standards/ADDONS.md` (new `## Ka0s-owned library repos` table); `AUDIT.md` (one process line);
`standards/README.md`.

**Verified problem.** LibKa0s is audited against this standard and is not on the roster
(`ADDONS.md:19-26` lists eight addons, none of them LibKa0s), so every addon-shaped rule is applied to it
and produces a finding the standard never meant — six of them (C13). Meanwhile the rules that genuinely
do bind it are scattered and unlabelled: `testing-§10`'s versioning suite, `testing-§11`'s kit-sync gate,
`localization-§5`, `automated-tests`, `lint`, `versioning-git`, and — by `testing-§10`'s own changelog
assertion — a root `CHANGELOG.md`.

**Change.**

1. `library-stack.md` §7 gains an *Applicability — what binds the library repo itself* block listing, by
   section name: **what applies** (`testing-§1`, `§9`, `§10`, `§11`, `lint`, `automated-tests`,
   `versioning-git`, `localization-§5`, `documentation-§5`, `documentation-§7` — a new machine needs the
   toolchain list as much for a library as for an addon); **what does not** (`documentation-§1`'s
   player-facing README structure and badge row, `documentation-§2`'s addon CLAUDE.md stub as written,
   `documentation-§3`'s `docs/` trio (`ARCHITECTURE.md`, `testing.md`, `smoke-tests.md`) and the five
   required topic-detail docs (`test-cases.md`, `performance.md`, `perf-runs/README.md`,
   `automated-tests/README.md`, `automated-tests/RESULTS.md`), `toc-file`, `options-ui`,
   `slash-commands`, `preview-mode`, `savedvariables`, `packaging`); and **what substitutes** — a root
   `CLAUDE.md` carrying `## Standards compliance (read first)` (the only one of `documentation-§6`'s
   three places that exists in a repo with no TOC and no player README), a root `DEPENDENCIES.md`, and a
   README pointer to the standard.
2. `ADDONS.md` gains a second table, `## Ka0s-owned library repos`, with LibKa0s and its folder and URL,
   and one sentence saying such a repo is in scope for the standards process and audited against
   `library-stack-§7`'s applicability list rather than the addon rule set.
3. `AUDIT.md` gains one process line telling the auditor to switch lists when the repo has no TOC.

**Findings unblocked:** C13's 6.

**Adoption cost downstream.** LibKa0s only (`M1-LK-13`): a root `CLAUDE.md` (S), a root `DEPENDENCIES.md`
(M — the toolchain is discoverable from the manifest but has never been written down), a README standards
reference (S). **No addon repo changes.**

**Effort:** M · **Risk:** low.

---

## M1-STD-08 · `documentation-§6` — one rule strength for standard citations

**File / section:** `standards/standards/documentation.md` §6 (new *Citing the standard* block).

**Verified problem.** The retired global `§N.M` numbering survives across the collection — 368 live sites
measured, of which five repos filed it and four (KickCD, PanelMaster, prettychat, LibKa0s) carry it
unflagged. The standard never says whether a citation inside a code comment is bound by the
`filename-§N` scheme, so each audit graded it differently — Medium against `documentation-§5` in two
repos, advisory-with-no-rule in two others — and two of them produced per-site counts that triage found
wrong in both directions. `wow-addon:revendor-standards` already claims the sweep, so the missing piece
is purely rule strength and reporting shape.

**Change.** A short *Citing the standard* block. A reference to the standard in any authored text the
repo owns — code comments, `.luacheckrc`/`.pkgmeta` headers, `docs/` pages — SHOULD use `filename-§N`.
A reference that **cannot resolve** is the defect, in two grades:

- Retired global `§N.M` notation is a **SHOULD**, swept mechanically.
- A **malformed or out-of-range** reference is a **MUST** fix, because it sends a reader to a section
  that does not exist. Live examples: `AbsorbTracker/settings/Slash.lua:199` `slash-commands-§:`;
  `BankLedger` `options-ui-§41`, `§190`, `§189` against a section with §1–§11; and — collection-wide —
  `standalone-windows-§2` and `packaging-§1`, cited by two bundles although neither file carries numbered
  subsections at all.

Frozen bundles under `docs/audits/`, `docs/reviews/` and `docs/automated-tests/` are evidence and MUST
NOT be swept — the same carve-out `standards/_raw/_industry/` already has. An audit records the sweep as
**one** rolled-up finding with the command that produces the current count, never a per-site enumeration,
since the enumeration is what went wrong in both audits that attempted it.

**Findings unblocked:** C15's 5 filed, plus the 4 unflagged repos.

**Adoption cost downstream.** Five or six addons run one mechanical sweep commit each (S), with the
out-of-range refs in BankLedger and the malformed one in AbsorbTracker fixed by hand. `M1-WA-07` widens
the sweeping command to match.

**Effort:** S · **Risk:** low.

---

## M1-STD-09 · Settle `CHANGELOG.md` — forbidden at root, written by the release command

**File / section:** `standards/standards/documentation.md` §1 (the root doc-set sentence at
`documentation.md:5`) and §3.

**Verified problem.** `documentation.md:5` says the repo root ships exactly three docs plus LICENSE —
a full `README.md`, a stub `CLAUDE.md`, and `DEPENDENCIES.md` — "and never a fourth doc". The
`wow-addon:bump-version` command, which `automated-tests-§6` and `performance-§10` both hang their
release checkpoints off, is specified to "write the CHANGELOG entry". ConsumableMaster ships a root
`CHANGELOG.md` and was written up High for it; triage's verdict was that the **contradiction**, not the
addon, needs resolving. It is not a one-repo curiosity: `testing-§10` makes a `CHANGELOG.md` effectively
mandatory in a library repo, since the versioning suite MUST assert that the changelog accounts for the
version every file is at — and LibKa0s duly ships one.

**Change.** Name `CHANGELOG.md` explicitly rather than leaving it to the count.

- **For an addon:** forbidden at root, because `documentation-§1` items 5 and 12 already carry the
  player-facing history in `## What's new` and `## Version History`, and a second history is the drift the
  never-a-fourth-doc rule exists to prevent. Say this in one sentence so the next audit cites a rule
  instead of a count.
- **For a Ka0s-owned library repo** (`M1-STD-07`'s applicability list): required, because `testing-§10`'s
  changelog assertion has nowhere else to look.

Then correct the release command's contract in the plugin (`M1-WA-09`) so it rolls `## What's new` and
`## Version History` for an addon and writes `CHANGELOG.md` only for a library repo.

**Ripple:** `EXECUTIVE_SUMMARY.md`'s root doc-set bullet — `README.md`, the `CLAUDE.md` stub,
`DEPENDENCIES.md`, plus `LICENSE` — gains the CHANGELOG clause.

**Findings unblocked:** `CM-A-26`.

**Adoption cost downstream.** ConsumableMaster deletes root `CHANGELOG.md` after folding anything
user-facing into `README.md` `## Version History` (S). **The real dependency is the plugin** — until
`M1-WA-09` lands, the next `bump-version` recreates the file. LibKa0s keeps its `CHANGELOG.md` and gains
a rule that says so.

**Effort:** S · **Risk:** low.

---

## M1-STD-10 · `testing-§9` — the suite list is the third ungated load list

**File / section:** `standards/standards/testing.md` §9 (third bullet, plus the closing paragraph).

**Verified problem.** §9 derives and pins two lists — the addon's own files from the TOC, and the
vendored library files in XML order — and is silent about the third: the ordered suite list handed to
`Kit.run`. The kit swallows its failure mode by design (`testkit/framework.lua:99`). AbsorbTracker carries
21 hand-written entries against 21 files on disk with nothing pinning the correspondence in either
direction, and the reference repo has the same hole in both of its lists
(`LibKa0s/tests/run.lua:17-19` and `:76-80`) while `testing-§10` names that repo as the reference
implementation for exactly this family of gates.

**Not "hand-maintained everywhere" — an earlier draft said so and it is wrong.** Two repos already ship
this gate and are the reference implementations to copy: **BankLedger** (`tests/run.lua:17`,
`tests/test_harness.lua:22-32`) and **PanelMaster** (`tests/run.lua:60-63`,
`tests/test_harness.lua:19-32`). **ConsumableMaster** has no declared list at all — `tests/run.lua:26-32`
auto-discovers — so it is outside the assertion's premise. The genuinely ungated declared lists are
AbsorbTracker's, KickCD's, LootHistory's, prettychat's, WhatGroup's and LibKa0s's own.

**Change.** A third bullet: the runner's **suite list** MUST be pinned by cases in both directions —
every `tests/test_*.lua` on disk appears in the list, and every listed path exists. Plus the matching kit
rule: `loadSuites` MUST report a listed-but-absent suite as a **skip with its reason** (`M1-LK-01`)
rather than silently omitting it, so the write-the-suite-later affordance survives while a renamed suite
stops disappearing without a trace. Extend §9's closing "both failure modes are silent" paragraph with
this third one.

**Findings unblocked:** `AT-R-05`, `LK-R-01`, `LK-A-09` (and it is the rule behind `M1-LK-04`).

**Adoption cost downstream.** Depends on `M1-LK-01`'s primitive. LibKa0s changes `loadSuites`,
re-vendors, and adds the two pinning cases (`M1-LK-11`). Each addon adds one small case pinning its suite
list against `ls tests/test_*.lua` (S). LootHistory, ConsumableMaster and PanelMaster additionally still
owe the existing §9 file-list obligations, which this does not change.

**Effort:** S · **Risk:** low.

---

## M1-STD-11 · `events-frames-taint-§8` — make the printer rule enforceable

**File / section:** `standards/standards/events-frames-taint.md` §8.

**Verified problem.** §8 bans feeding chat/debug args through `..` / `tostring` / `table.concat` before
the shared printer and says a site is non-compliant "even if it is never handed a secret today". Roughly
**50 sites** exist collection-wide — 18 in AbsorbTracker (`settings/Slash.lua:33,97,242,246,282,321,334,
339,344,352,357,365,389,414,427,428,439` and `settings/Schema.lua:214`), ~25 in PanelMaster, plus KickCD
and WhatGroup — and `.luacheckrc` cannot see any of them. Triage found every one latent: PanelMaster reads
no combat-protected API at all, and no `UnitGetTotalAbsorbs` value reaches any AbsorbTracker site. An
unenforceable MUST at 50 sites produces a recurring finding and no behavior change.

**Change — pick one of two, and say which in the section.**

- **(a) Scope the MUST** to sites that can receive a value from a combat-protected API, with a named list
  of those APIs, and demote the rest to a SHOULD with the drift rationale attached; **or**
- **(b) Make compliance cheaper than the bypass** — have LibKa0s ship a varargs printer
  (`NS.Print("%s = %s", k, v)`) so the compliant form is as short as the concatenation, and keep the MUST
  unscoped once that exists.

Option (b) is the better long-run answer; option (a) is one edit here. Either way the section MUST stop
being a rule that 50 sites break with zero reachable risk.

**The fork is not free and must be resolved before Milestone 1 begins.** The two branches differ by roughly
two orders of magnitude in cost: (a) is one paragraph in the standard plus a re-grade, and `M4-27` becomes
a disposition; (b) requires **`M1-LK-15`** — the varargs printer on the `Core.lua` seam — with its own minor
bump, API document, `tests/test_versioning.lua` pairing, inclusion in `M1-LK-14`'s release, and a re-vendor
into all eight addons before a single call site can be converted. `M1-LK-15` is written into Group A as
**CONDITIONAL** precisely so option (b) does not break the plan's hard rule that every upstream change is
in Milestone 1. Under (a), Milestone 1 has 41 items and the plan has 96; under (b), 42 and 97.

**Findings unblocked:** C11's 6 (`AT-A-03`, `BL-A-09`, `KCD-A-04`, `KCD-A-15`, `PM-A-08`, `WG-A-08`) —
except `BL-A-09`, which is a **real** bare global `print()` and is fixed in Milestone 2 regardless.

**Adoption cost downstream.** Under (a): four repos re-grade and the sites stay. Under (b): four repos
rewrite ~50 call sites mechanically (M each) after a LibKa0s minor bump and re-vendor.

**Effort:** M · **Risk:** low.

---

## M1-STD-12 · An applicability condition for `architecture-§4`

**File / section:** `standards/standards/architecture.md` §4.

**Verified problem.** `architecture-§4` — "Modules MUST communicate via named messages, not direct calls."
Its whole rationale is the CallbackHandler same-target clobber hazard, which **cannot arise** with one
feature module and zero event traffic. prettychat has exactly that shape
(`docs/ARCHITECTURE.md:119` "There is no message bus."; direct calls at `modules/Override.lua:108-109,
120-121, 138-139`) and is filed as a MUST failure. The rule states no applicability condition, so it is
unsatisfiable in principle for a single-module addon: there is no second party to name a message to.

**Change.** `architecture-§4` gains a scope sentence: the MUST binds an addon with two or more feature
modules or any module registering game events; below that, direct calls are permitted and the
`## Message Bus` section of `docs/ARCHITECTURE.md` records that there is none and why.

**On the evidence base, stated rather than glossed.** The only finding behind this is `PC-A-12`
(prettychat, Low), and the bar for changing a collection-wide normative document on one repo's row is high
— `M1-STD-02`'s deviation register exists exactly to absorb rows like it. It is kept here anyway because
the defect is in the **rule**, not in the addon: a MUST that no single-module addon can satisfy will be
re-filed against every future single-module addon, and a register row per addon is the wrong shape for a
rule that is wrong once. That is not true of the paragraph below, which is why it was dropped.

**Dropped from this item: the `events-frames-taint-§1` carve-out.** An earlier draft also carved a
permanent exception into `events-frames-taint-§1` for unit-filtered registration, on the evidence of
`AT-A-10` — one **Info** row, in one repo, whose justification is already written down at
`AbsorbTracker/docs/ARCHITECTURE.md:316-331`, exactly where the process asks. A written, sound, in-place
justification for a single repo is the textbook input to `M1-STD-02`'s register, not to a permanent
scope sentence in a shared normative document that every other addon will read. `AT-A-10` is re-routed to
an `M3-08` register row with a re-check trigger (a future client build where `RegisterUnitEvent` accepts
more than two tokens). If a second repo's evidence ever supports the carve-out, it can be made then,
additively.

**Findings unblocked:** `PC-A-12`.

**Adoption cost downstream.** prettychat records one paragraph, which it already has; the row stops
recurring.

**Effort:** S · **Risk:** low.

---

## M1-STD-13 · `localization` — English-only as a terminal state

**File / section:** `standards/standards/localization.md` §1 and §3.

**Verified problem.** Four repos independently reached the same conclusion, and all four met both MUSTs
(seam exported, `enUS.lua` ships) while leaving the SHOULD open: `AbsorbTracker/locales/enUS.lua` is 12
lines with no populated keys and is deferred as PLAN-02; `PanelMaster/locales/enUS.lua:8-14` documents the
0.1.0 English-only scope decision explicitly; prettychat concatenates four settings strings
(`settings/Schema.lua:72-73`, `settings/Panel.lua:168`, `:393`) and ships `enUS.lua` only;
`WhatGroup/locales/enUS.lua:67-70`, `:104` carry five dead keys. **A SHOULD that four of eight adopters
decline the same way is mis-specified.**

**Change.** Say that routing user-facing strings through `NS.L` is a SHOULD whose **terminal compliant
state** is either (a) strings routed, or (b) an English-only decision recorded in the deviation register
(`M1-STD-02`) with its re-check trigger — the first non-English locale file. Both MUSTs stay. An addon in
state (b) is compliant, not open.

**Findings unblocked:** `AT-A-09`, `PC-R-06`, `PM-A-17`, `WG-R-06`.

**Adoption cost downstream.** Four repos add one register row each (S). WhatGroup additionally deletes
five dead keys.

**Effort:** S · **Risk:** low.

---

## M1-STD-14 · Reconcile `performance-§2`'s idiom with `Perf.lua`'s API

**File / section:** `standards/standards/performance.md` §2 and §3.

**Verified problem.** `performance-§2` specifies the bracket idiom as
`local t0 = Perf.on and debugprofilestop()` — **no call** on the dormant path — while
`LibKa0s/Perf.lua:378-379` documents `P.Open`/`P.Close` as costing "one boolean test and nothing else",
when `:400-403` and `:407-410` are two real Lua calls. The library and the standard specify different
shapes for the same job. Consumers are graded against §2 (`CM-A-07`'s per-call `KCM.Perf` lookup;
`KCD-R-05`'s unclosed early-return exits), and §3's containment declaration has no verification at all
(`AT-R-01`).

**Change.**

1. §2 names **both** shapes and when each applies: the inline form for a single-exit hot path where the
   dormant cost must be exactly one boolean test; the `P.Open`/`P.Close` pair for a multi-exit region,
   with its real cost stated (two calls plus the test) so nobody claims otherwise. Keep the load-time
   upvalue requirement in both.
2. §3 requires that a declared `within` be **verifiable**: the record MUST carry observed containment
   beside the declared value (`M1-LK-08`), and a bracket MUST be closed on every exit — with the
   corollary that an unbalanced bracket is a defect the library reports rather than a silent undercount.

**Findings unblocked:** the C9 group in full — `AT-R-01`, `CM-A-07`, `CM-A-08`, `CM-A-13`, `KCD-R-05`,
`KCD-A-18`, `LK-R-04`, `LK-R-05`, `LK-R-06`.

**Adoption cost downstream.** Sequence **before** any addon bracket-shape fix — the two currently
specify different shapes, so fixing an addon against the wrong one is rework.

**Effort:** S · **Risk:** low.

---

## M1-STD-15 · `toc-file-§1` category enumeration; unnumbered-section references

**File / section:** `standards/standards/toc-file.md` §1 (`toc-file.md:19`); a note in
`documentation.md` §6 (with `M1-STD-08`).

**Verified problem, three parts.**

1. `toc-file.md:19` shows `## Category-enUS: <Combat|Group|Auction|Chat|UI|Misc>`.
   `prettychat/PrettyChat.toc:10` reads `Chat & Communication`, which is a **real Blizzard addon-category
   string**. Narrowing the TOC to `Chat` would list the addon under a category Blizzard does not use, so
   the standard's six-value enumeration is the incomplete half.
2. Five section files carry **no numbered subsections** — `lint.md`, `packaging.md`, `preview-mode.md`,
   `standalone-windows.md`, `audit-review-history.md` — yet bundles cite `standalone-windows-§2` and
   `packaging-§1`. Under `filename-§N` those cannot resolve, and `M1-STD-08` makes an unresolvable
   reference a MUST fix. The standard should say which files are referenced by bare filename.
3. **`toc-file-§5`'s file-listing code block is read as an ordered MUST for the files *inside* a section.**
   It is not. §5's MUSTs are the **section-header** order — Libraries → Locales → Core → Defaults →
   Modules → Settings — and a single trailing newline. The code block's within-`core/` sequence
   (`Compat → Constants → State → Util → PerfSetup → Database → <Addon>`) is a reference implementation,
   and it is not achievable in an addon whose `Namespace.lua` bootstraps the `NS` table that
   `Compat.lua` and `Constants.lua` then attach to. ConsumableMaster's audit filed exactly that as a MUST
   (**CM-49** / `CM-A-16`) against `ConsumableMaster.toc:48-58`, whose ordering is justified in the TOC's
   own comments at `:44-47` and `:53-55`.

**Change.** Replace the enumeration with Blizzard's actual category set, or state that the list is
illustrative and the value MUST be a string Blizzard's client accepts. In `documentation-§6`'s new
block, list the section files that carry no numbered subsections and are therefore always referenced by
bare filename. And add one sentence to `toc-file-§5` stating that the within-section file sequence in the
code block is **illustrative**, that the normative requirement is the section-header order, and that an
addon whose bootstrap requires a different within-section order records the reason in a TOC comment.

**Findings unblocked:** `PC-A-22`, plus the correctness of every `standalone-windows` and `packaging`
reference in the ledger. Part 3 is the rule half of `CM-A-16`, whose repo half is an `M3-08` register row.

**Adoption cost downstream.** None — prettychat's TOC and ConsumableMaster's TOC are both already correct;
the standard moves to them.

**Effort:** S · **Risk:** low.

---

## M1-STD-16 · v2.22.0 rollup

**File / section:** `standards/STANDARDS.md` — version and date at `:1`, a changelog entry at the top, the
**Sections** map if any file gains a section, and the anti-pattern range `#1–#55` → `#1–#56`;
`standards/EXECUTIVE_SUMMARY.md`; `standards/NEW_ADDON_CONTEXT.md`; `AUDIT.md`, `AUTOMATED_TESTS.md`,
`NEW_ADDON.md` where a playbook's process line changes.

**Change.** Bump v2.21.0 → v2.22.0 with one changelog entry naming every section touched by
`M1-STD-01` … `M1-STD-15` and `M1-STD-17`. `performance` gains §12; `anti-patterns` gains #56;
`documentation`, `testing`, `automated-tests`, `library-stack`, `architecture`, `localization`,
`toc-file`, `events-frames-taint`, `audit-review-history`, `ADDONS.md` and `AUDIT.md` are edited in place.
Every count claim written into these documents names its members, per the repo's own editing rule.

**This is the last STD item.** Doing it earlier means doing it twice.

**Findings closed here:** none directly; it is what makes the other sixteen citable.

**Effort:** S · **Risk:** low.

---

## M1-STD-17 · `AUDIT.md:91` — grade by impact, and collapse derived rows

**File / section:** `WowAddonStandards/AUDIT.md:91` (step 5, *Catalog deviations*), plus the matching
sentence in `audit-review-history.md` if it restates the severity contract.

**Verified problem — the plugin edit that would otherwise be overridden at runtime.** `M1-WA-03` adds a
`### Grading a deviation` rule to `wow-addon/agents/standards-audit.md`: severity is **impact, not rule
strength**, and derived dependents are listed as `derived from <ID>` and excluded from the headline tally.
That edit does not take effect. `wow-addon/agents/standards-audit.md:44` states plainly: *"If this list and
the fetched `AUDIT.md` ever disagree, **the fetched playbook wins**."* And `AUDIT.md:91` still reads:

> One row/entry per gap: the ID, the section violated, **MUST/SHOULD severity**, a one-line description,
> and the fix direction.

No `M1-STD-01` … `M1-STD-16` item touches that sentence — `M1-STD-16`'s change column only promises to
ripple into `AUDIT.md` "where a process line changed". So the plugin authors the new grading rule and the
playbook overrides it on the next run, and every acceptance criterion resting on it is unmet: `M5-01`'s
"`M1-WA-03`'s grading rule is what makes that true", and the plan's own "a fresh audit's MUST tally is
under five rows".

**Change.** Replace `AUDIT.md:91`'s "MUST/SHOULD severity" with the impact-graded form: the ID, the section
violated (as `filename-§N`), the **impact grade** (High only for what a user, their SavedVariables or their
session can hit today; a doc-only or config-only MUST failure is Low or Info **and still names its MUST**),
a one-line description, and the fix direction. Add the one-root rule: a deviation derived from an unadopted
subsystem is filed as `derived from <ID>` and excluded from the headline tally, with the graduation
criteria stated.

**Verified by.** `grep -n "impact, not rule strength" AUDIT.md` resolves.
`grep -n "MUST/SHOULD severity" AUDIT.md` returns nothing. `M1-WA-03`'s dependency column points here.

**Findings closed here:** none directly; it is what makes `M1-WA-03`, `M5-01` and the plan's MUST-tally
acceptance criterion actually hold.

**Dependencies:** none. **`M1-STD-16` rolls it up** alongside `M1-STD-01`…`-15`.
**Effort:** S · **Risk:** low.

---

# Group C — the `wow-addon` plugin

Path: `/mnt/d/Profile/Users/Tushar/Documents/GIT/wow-addon`
16 commands under `commands/`, 2 agents under `agents/`.

**No plugin item closes a finding by itself.** Each one stops a class from regenerating, or unblocks
addon work that would otherwise be undone by the next command run.

---

## M1-WA-01 · Set the runner's executable bit in the git index, not the working tree

**File / section:** `commands/new-addon.md:16` (step 1 of "Automated test records — scaffold them with the
addon"); `commands/automated-tests.md:39-40` (Step 1's third bullet).

**Verified problem.** Both instructions say `chmod +x` — `new-addon.md:16` "…and
`chmod +x tests/_kit/run-automated-tests.sh`", `automated-tests.md:39` "If it is present but **not
executable**, `chmod +x` it". That instruction is inert here in both directions: all nine repos have
`core.fileMode=false`, and the tree is DrvFs where every file reports `rwxrwxrwx`, so the presence check
never fires and a `chmod` that did fire would be ignored by git. Result: `100644` in 9/9 repos, including
LibKa0s's `testkit/` source.

**Change.** Replace the bare `chmod +x` with `chmod +x tests/_kit/run-automated-tests.sh` **and**
`git update-index --chmod=+x tests/_kit/run-automated-tests.sh`, then verify with
`git ls-files -s tests/_kit/run-automated-tests.sh` and require mode `100755`. Replace the working-tree
presence test with the index-mode test as the condition, and state the reason inline. `revendor-standards`
has no kit-vendoring step today, so leave it alone.

**Findings unblocked:** C18's 4 filed, plus the 5 unfiled.

**Adoption cost downstream.** One `git update-index --chmod=+x` plus a commit in each of eight addons.
No code, docs or tests change. **The upstream half is not fixable from here** — `LibKa0s/testkit/` is
itself `100644`, so `M1-LK-06` must land or every future re-vendor re-imports 644.

**Effort:** S · **Risk:** low.

---

## M1-WA-02 · `revendor-standards` sweeps normative-claim drift; `new-addon` scaffolds both checkpoints

**File / section:** `commands/revendor-standards.md` — new subsection **3f** after `### 3b. Retired forms,
swept out of every doc` (`:76-78`), added to the Step 4 apply-automatically list;
`commands/new-addon.md` step 3.

**Verified problem.** Nine of nine repos state the commit gate and are silent about the release gate —
one template, not nine drifts. `docs/automated-tests/README.md` is byte-identical across AbsorbTracker,
LootHistory, PanelMaster and prettychat down to the line numbers (`## What gates, and what only records`
at `:19`, the `perf … no — recorded only` row at `:25`), and `docs/testing.md` carries the same sentences
in all eight addons. `new-addon.md` step 3 is the origin — "Create docs/automated-tests/README.md (what it
is, how to run it, which suites gate)" with no checkpoint distinction. `revendor-standards.md`'s Step 3b
sweep covers retired notation, dead section filenames, unnamed count claims and the retired drop-in
label — **a doc paraphrasing a section the standard has since changed is not on the list**, so the sweep
runs clean over all nine repos.

**Change.**

1. New **3f — normative claims the standard has since changed**, scoped to statements about *which
   checkpoint gates on what*, naming the three target locations explicitly: `docs/testing.md`'s Gates?
   table and its "Commits are gated on…" paragraph, `docs/automated-tests/README.md` § "What gates, and
   what only records", and any `CLAUDE.md` sentence of the form "complexity — recorded, never a gate".
   The rewrite is mechanical and fully determined by the fetched section: a gate statement MUST name its
   checkpoint, so "perf and complexity never fail a run" becomes "…never fail a *run*; the *tag* is gated
   on all four suites plus zero functions above CCN 15, evaluated by `/wow-addon:bump-version` from the
   run's `manifest.json`".
2. `new-addon.md` step 3: the scaffolded `docs/automated-tests/README.md` and `docs/testing.md` gate table
   MUST state both checkpoints, taking wording from the fetched `automated-tests-§3` rather than from the
   pack's summary sentence.

**Findings unblocked:** C8's 9, jointly with `M1-LK-07`.

**Adoption cost downstream.** Eight addons plus LibKa0s take a two-sentence doc edit each, applied by
re-running the command — no code, no tests, no version bump. **Honest limit:** the third statement of the
same claim is generated. `LibKa0s/testkit/run-automated-tests.sh:372` emits the `RESULTS.md` lead-in on
every run, so the sweep cannot fix it and would be overwritten if it tried. The sweep's report **must say
so** rather than appear to have finished the job.

**Dependencies:** should land after `M1-STD-05` so the target wording is normative. **Effort:** M · **Risk:** low.

---

## M1-WA-03 · Grade audit deviations by impact; collapse derivative rows under their root

**File / section:** `agents/standards-audit.md` — new `### Grading a deviation` between the "Follow
AUDIT.md" list and "The shared subsystems are a library".

**Verified problem.** `agents/standards-audit.md:40` asks for "MUST/SHOULD severity" and nothing else, and
`AUDIT.md:91` says the same. Across the collection almost every audit row was filed High and almost every
one was downgraded, with triage's rationale repeating itself ("a missing doc is Low by definition";
"doc-only, so Low despite the MUST marker"). The second half is worse: an unadopted subsystem generates a
fan of independent High rows — BankLedger `BL-11`…`BL-18`, LootHistory `LH-20`…`LH-26`, PanelMaster
`PM-001`…`PM-012`, prettychat `PC-40`…`PC-44`, WhatGroup `WG-30`…`WG-35` — each fan containing one
decision and six or seven mechanical consequences, several of which the audits themselves concede would
be worse to fix in isolation.

**Change.** Two rules.

- **Severity is impact, not rule strength.** High is reserved for something a user, their saved variables
  or their game session can hit today; a MUST failure that is doc-only, config-only, or has no reachable
  consequence in the current code is Low or Info — and the row still says which MUST it is against, so
  nothing is lost by the lower grade.
- **One root, derived dependents.** When several rows follow from one unadopted subsystem or one absent
  file, file the root as its own row and list the dependents beneath it as `derived from <ID>`, excluded
  from the headline MUST tally. A dependent that is independently fixable **and** independently useful
  graduates to its own row and says why.

**Findings unblocked:** the counting artifacts across C1 and C4 — roughly 45 rows stop being re-filed at
MUST strength every cycle.

**Adoption cost downstream.** No addon file changes. The next audit in each of nine repos produces a
shorter, honestly-graded `02_DEVIATIONS` and a headline count that means something; frozen bundles stay
frozen.

**Hard dependency, not a coordination note.** `AUDIT.md:91` specifies only MUST/SHOULD severity, and
`agents/standards-audit.md:44` says **the fetched playbook wins** on conflict — so this edit is *inert*
until `AUDIT.md` carries the same rule. That edit is scoped as its own item, **`M1-STD-17`**, rather than
left to `M1-STD-16`'s "where a process line changed" ripple, which would not have fired: no
`M1-STD-01`…`-15` item touches the severity sentence. **`M1-WA-03` depends on `M1-STD-17`.**

**Effort:** M · **Risk:** low.

---

## M1-WA-04 · Read the deviation register before filing a MUST as open

**File / section:** `agents/standards-audit.md` — new bullet in "Mechanical checks — run them, don't
reason about them".

**Verified problem.** Addons record accepted deviations in `docs/pending/LEDGER.md`,
`docs/ARCHITECTURE.md` § "Documented deviations", `docs/scope.md`, and `CLAUDE.md` paragraphs
(prettychat `CLAUDE.md:5-13`, PanelMaster `CLAUDE.md:36`, ConsumableMaster `docs/scope.md:20`).
`agents/standards-audit.md` mentions none of them; neither does `AUDIT.md`. So settled — in one case
user-signed — decisions are re-litigated at MUST strength: BankLedger's missing `defaults/Profile.lua` is
filed High although ratified at `docs/ARCHITECTURE.md:568-581`; WhatGroup's Perf decline is filed High
although `docs/pending/LEDGER.md:63` records it decided 2026-08-02 with sign-off. **The inverse case is the
finding that actually matters and is currently invisible:** BankLedger's Perf decline lives only in
`LEDGER.md:65` with no ARCHITECTURE register entry, and that missing entry — not the code — is the live
gap.

**Change.** Read the register first, naming `docs/pending/LEDGER.md`, `docs/ARCHITECTURE.md` § Documented
deviations, root `CLAUDE.md` accepted-deviation notes, and any `docs/scope.md`. A deviation carrying a
written, reasoned decision is filed as a **recorded deviation** with its ledger id and decision date, not
as an open MUST failure, and does not count toward the MUST tally — unless the audit has new evidence the
reasoning is now wrong, which it states. Conversely, a decline recorded in `LEDGER.md` with **no**
register entry is itself the deviation to file, because the ledger is a working queue and
`ARCHITECTURE.md` is where a reader looks.

**Findings unblocked:** C4's 13, plus `BL-A-01`, `BL-A-02`, `LH-A-20`, `PM-A-01`, `AT-A-09`.

**Adoption cost downstream.** No addon change required to adopt. Two repos gain one paragraph each as a
consequence of the inverse rule — BankLedger and LootHistory each need a register entry for a Perf
decline currently recorded only in their ledgers.

**Dependencies:** `M1-STD-02` defines the register. **Effort:** S · **Risk:** low.

---

## M1-WA-05 · Require a citation-verification pass before either agent writes its bundle

**File / section:** `agents/standards-audit.md` (the `03_EVIDENCE` bullet); `agents/review.md` (the
"A finding backed by a measurement cites it" bullet under `01_FINDINGS.md`).

**Verified problem.** Both agents demand `file:line` evidence and neither demands the cited line be
re-read. The cost shows up in nearly every bundle: AbsorbTracker's audit counted 17 pre-formatted chat
sites in `02_DEVIATIONS` and 18 in its own execution plan (the real number is 18), and reported 31 retired
notation hits against roughly 50 because the sweep never covered the live `docs/` pages; BankLedger's
audit listed nine bad refs, one of them a frozen ledger row that should not count and one real hit at
`LEDGER.md:64` that it missed; ConsumableMaster's cited `settings/Panel.lua:507`/`:711` for locals used at
`:502-503`/`:734`, and `.luacheckrc:74` for a comment at `:66`; KickCD's cited
`modules/IconGrid_Render.lua:826`, the function header; LootHistory's cited `.luacheckrc:60` for `:43`.
Reviews are no better — one cited `modules/Collector.lua:494` in a 221-line file, two cited the `test(`
declaration lines instead of the guard, and one built a consistency argument on a three-item comparator
list of which one item was wrong.

**Change.** In both agents: before the bundle is written, **re-read every `file:line` the bundle cites and
quote the cited text beside it** — a citation that does not resolve to the claimed content is corrected or
dropped, never shipped. Second half, both files: **every count is produced by a recorded command**, with
the exact invocation and its output pasted into the evidence file, **and the command's scope stated** —
most of the miscounts above came from a sweep that silently excluded `docs/` or `tests/`, and a count
without its scope is not a count.

**Findings unblocked:** none directly. It is what stops the next triage pass spending itself re-deriving
line numbers.

**Adoption cost downstream.** Nothing changes in any addon. Each audit and review run gets modestly
longer by one re-read pass over citations it already collected.

**Effort:** M · **Risk:** low.

---

## M1-WA-06 · `bump-version` writes the perf-skip exception into the release notes

**File / section:** `commands/bump-version.md` Step 4 (the CHANGELOG and README-highlights paragraphs);
Step 5 item 3's pointer; the Hard rules list.

**Verified problem.** `automated-tests-§3` grants exactly one exception to the release gate — `perf`
skipped because the addon ships no `tests/perf.lua` — and MUSTs that it be stated in the release notes.
`bump-version.md` states the obligation twice (Step 2 item 3 at `:62-64`: "MUST be stated as such in the
Step 6 report and the release notes"; Step 5 item 3) but never operationalizes it: **Step 4 is the step
that authors the CHANGELOG entry, the README "What's new" body and the Version History row, and it carries
no instruction to insert the sentence**, while Step 5 item 3 redirects to the Step 6 chat report. Five
addons are permanent perf-skippers — BankLedger, KickCD, LootHistory, PanelMaster, WhatGroup — and none
of their README release sections says so.

**Change.** Add a rule to Step 4: when Step 2 recorded the perf gate as satisfied by the no-scenarios
exception, the release notes carry one sentence saying so — the addon ships no `tests/perf.lua`, so the
perf suite was skipped and this release's gate covered lint, tests and complexity only. Fix Step 5 item 3
to name Step 4 (the notes) as well as Step 6 (the chat report), and add the omission to the Hard rules
list beside "Don't let the generated text outrun the commits".

**Findings unblocked:** `LH-A-24` (the one C1 member with a live consequence today), and the residual
obligation behind `WG-A-05`, `KCD-A-13`, `PM-A-04`, `PM-A-13`, `BL-A-07`.

**Adoption cost downstream.** Five repos get one sentence in their **next** release entry. Nothing
retroactive — the command already refuses to edit past CHANGELOG entries or Version History rows.

**Effort:** S · **Risk:** low.

---

## M1-WA-07 · Sweep notation outside `docs/`, and range-check `§N`

**File / section:** `commands/revendor-standards.md` Step 3b (`:76-78`); the "Documentation only. Never
edit `.lua`, `.xml`, or any code" hard rule.

**Verified problem.** `revendor-standards.md:78` says "Grep the repo's **docs**", so the sweep never looks
at code, tests or config — where most surviving retired notation lives. AbsorbTracker has ~25 `§N.M` hits
across `core/ settings/ modules/ defaults/ locales/ tests/` (`core/Constants.lua:11`,
`core/AbsorbTracker.lua:9, :38, :63, :163`, `defaults/Profile.lua:5, :8`); ConsumableMaster 34 in code
comments; BankLedger in `settings/OptionsSetup.lua:43`, `settings/Schema.lua:184`, `settings/Panel.lua:58`,
`tests/test_panel.lua:175`; LootHistory in `settings/OptionsSetup.lua:101`, `tests/test_database.lua:390`;
WhatGroup in `.luacheckrc:1` and `.pkgmeta:4`. The command also has **no validity check on the new
notation**, so it passes over `options-ui-§41`, `§190`, `§189` (that section has §1–§11) and the malformed
`slash-commands-§:` at `AbsorbTracker/settings/Slash.lua:199`. It already fetches every section file, so it
holds exactly the data needed to range-check.

**Change.** Change the grep scope from the repo's docs to the whole repo **excluding** `libs/`,
`tests/_kit/`, `docs/audits/`, `docs/reviews/` **and `docs/automated-tests/`** — all three `docs/` paths are
frozen evidence, exempt by `M1-STD-08` and by this plan's invariant 2, and an earlier draft named only the
first two. The omission is not theoretical: KickCD carries **30** `§N.M` lines inside frozen
automated-test bundles (`20260804-182144/`, `-214315/`, `-233245/`, in `test-cases.md` and `tests.txt`), so
`grep -rEn '§[0-9]+\.[0-9]' KickCD` under the earlier exclusion list returns 30, not 0 — a criterion that
can only be met by corrupting evidence. Measured: 69 hits with the two-path exclusion, **39** with all
three. Add a third sweep item — **out-of-range and malformed `filename-§N` references**: count each
fetched section file's local `§` headings and flag any reference whose N exceeds it, plus any ref with an
empty or non-numeric N. Keep the edit boundary intact: docs hits apply automatically as today; code and
config hits are reported with `file:line` and applied only on explicit user confirmation, as a
**comment-only** edit. Amend the "never edit code" hard rule to name that one confirmed comment-only
exception rather than leaving the rule and the new behavior in contradiction.

**Findings unblocked:** C15's 5 filed, plus the 4 repos carrying it unflagged (KickCD 39, PanelMaster 1,
prettychat 1, LibKa0s 183).

**Adoption cost downstream.** Comment-only edits in five to nine repos, roughly 368 sites in total —
LibKa0s (183) and AbsorbTracker (83) being the bulk — all counted **outside** `libs/`, `tests/_kit/` and
all three frozen `docs/` paths. No behavior change, no test movement, no version bump.

**One scoping trap in LibKa0s, called out here because `M3-07` cannot fix it.** Two of LibKa0s's hits are
in its **shipped** source — `LibKa0s/LibKa0s/Options.lua:129` and `:173` ("…exactly what Ka0s standard
§3.4 exists to stop") — and that file is vendored byte-for-byte into all eight addons
(`diff -q LibKa0s/LibKa0s/Options.lua AbsorbTracker/libs/LibKa0s/Options.lua` → identical). Sweeping them
in `M3-07`, after `M3-01`'s re-vendor, would redden all eight consumers' `tests/test_vendor_sync.lua`
against a payload they may not legally patch (invariant 3), with no second re-vendor scheduled. **Those two
sites belong to `M1-LK-10`**, whose commit already changes shipped bytes and which `M1-LK-14` releases;
`M3-07` must not touch `LibKa0s/*.lua`.

**The real cost is the boundary:** this command's blanket "never edit code" rule exists so an agent
editing every addon's `CLAUDE.md` cannot also reach into `.lua`, and relaxing it — even to comments, even
behind a confirmation — should be reviewed as the design decision it is, not as a sweep widening.

**Dependencies:** `M1-STD-08` sets the rule strength. **Effort:** M · **Risk:** medium.

---

## M1-WA-08 · Reachability line on every review finding, and severity capped by it

**File / section:** `agents/review.md` — the severity buckets at `:244-245` and the `01_FINDINGS.md`
finding-format bullet.

**Verified problem.** `agents/review.md:244-245` defines Critical and High by defect *kind* — "data loss,
taint propagation…", "functional bug, deprecated API…" — with nothing about who can reach the defect. The
bundles graded accordingly and triage moved almost all of them: two prettychat findings filed Critical for
a format-string arity defect that shows a wrong chat line (down to High); BankLedger's `/bl debug`
LibStub-key typo filed High for a developer-only diagnostic verb; KickCD's inert color picker filed High
for one cosmetic setting whose default is already the value it paints; four repos filed the vacuous
vendor-sync gate at High or Medium when it is test-inventory integrity rather than shipped behavior.
**Note the rule that does not work here:** ConsumableMaster's `CM-A-25` and PanelMaster's `PM-R-01` were
both filed High on a degraded path and both *confirmed* High, so a blanket "degraded paths cap at Medium"
would be wrong.

**Change.** Require every finding to carry an explicit **Reachability** line: who hits this, in what
configuration, today. Then bind severity to it — a finding whose reachability reads *developer-only verb*,
*comment or doc text*, *test inventory only*, or *unreachable in any shipping configuration* cannot be
graded High; Critical requires data loss, taint propagation, secret-value leakage, or a failure to load a
normal install reaches. This keeps a genuinely High degraded-path defect at High (its reachability line
reads "any install where the library fails LibStub's floor — a session-long error loop") while pulling the
diagnostic-verb and comment findings down where they belong, and makes the grade auditable rather than a
matter of taste.

**Findings unblocked:** none directly; review bundles only. Existing frozen bundles are untouched.

**Effort:** S · **Risk:** low.

---

## M1-WA-09 · `bump-version` surfaces the `CHANGELOG.md` conflict instead of quietly maintaining it

**File / section:** `commands/bump-version.md` Step 4 (CHANGELOG paragraph) and Step 6 (the report).

**Verified problem.** `documentation.md:5` says the root ships exactly three docs plus `LICENSE` — a full
`README.md`, a stub `CLAUDE.md`, and `DEPENDENCIES.md` — and never a fourth. `bump-version` advertises "write the CHANGELOG entry for everything since the last tag" and
Step 4 fills a root `CHANGELOG.md` in full when one exists. `CM-A-26` was filed against the addon; triage's
read is that the addon is not what needs fixing. Today the plugin is the half that entrenches the
contradiction: it maintains the file every release and says nothing. Of the roster addons, exactly one —
ConsumableMaster — has a root `CHANGELOG.md`; LibKa0s has one too but is not on the roster.

**Change.** Keep both existing behaviors — do not create a `CHANGELOG.md`, and do fill one that exists —
but add a line to the Step 6 report: when a root `CHANGELOG.md` was written, state once that it is a
standing `documentation-§1` conflict (root is `README.md`, the `CLAUDE.md` stub, `DEPENDENCIES.md` and
`LICENSE`), that this command maintained it because it is the user's file, and that resolving it is an
upstream decision. Mirror the note in the Step 4 CHANGELOG paragraph so the reason travels with the
behavior. Once `M1-STD-09` lands, replace the note with the resolved rule: roll `## What's new` and
`## Version History` for an addon, write `CHANGELOG.md` only for a library repo.

**Findings unblocked:** `CM-A-26`, jointly with `M1-STD-09`.

**Adoption cost downstream.** One repo sees one extra report line per release; no file changes. **Until
this lands, `M3-11` cannot hold** — the next `bump-version` recreates the file ConsumableMaster deleted.

**Dependencies:** `M1-STD-09`. **Effort:** S · **Risk:** low.

---

## M1-WA-10 · `sync-docs` gains a comment-citation gate

**File / section:** `commands/sync-docs.md` — new check alongside count-claim verification, command/script
parity and dead-export detection.

**Verified problem.** C3 is thirteen findings across eight repos and its root cause is that **nothing ties
a comment's named file or caller to reality**. `sync-docs` already verifies count claims, command parity,
config drift and dead exports in *documentation* — it never looks at code comments. Live examples:
`AbsorbTracker/modules/Bar.lua:5-6` and `:86-87` name `core/DebugLog.lua`, deleted;
`PanelMaster/core/CoreSetup.lua:21` names `modules/DebugLog.lua`, deleted;
`KickCD/settings/Slash.lua:211` cites `settings/Slash.lua:383` in a 347-line file;
`LootHistory/settings/Slash.lua:111-112` names `settings/Panel.lua` as a reader of two symbols it never
references; `AbsorbTracker/core/Units.lua:78-85` names the slash CLI as the sole caller of a function with
zero callers anywhere.

**Change.** Add a **comment-citation** check: extract path-like tokens and `Symbol.Member` references from
comments in the addon's own source (excluding `libs/` and `tests/_kit/`), and report those where the named
path does not exist, or where a grep for the named symbol finds no call site. Report with `file:line`;
apply only on confirmation, as a comment-only edit — the same boundary `M1-WA-07` establishes.

**Findings unblocked:** C3's eleven addon-side members (`AT-R-11`, `BL-R-05`, `BL-R-07`, `CM-R-11`,
`CM-R-13`, `KCD-R-09`, `KCD-R-10`, `LH-R-07`, `PM-R-09`, `PM-R-10`, `PC-R-10`) and, going forward, the
class.

**Adoption cost downstream.** Comment-only edits in eight repos; no behavior change and no test movement.

**Sequenced as a recurrence guard, not as a gate on `M4-10`.** An earlier draft made `M4-10` — eleven
one-line comment corrections whose exact `file:line` is already enumerated in that item — unstartable until
this plugin feature shipped, and made its only acceptance criterion "the comment-citation check reports
zero unresolvable references". That inverts the ordering the rest of the plan uses, where M2's
user-visible defects deliberately carry no M1 dependency. **`M4-10` now depends on nothing** and verifies
against evidence it already carries; this item lands **after** `M4-10` and stops the class from coming back.

**Dependencies:** shares the code-edit boundary decision with `M1-WA-07`. Sequenced after `M4-10`.
**Effort:** M · **Risk:** medium.

---

# Milestone 1 exit criteria

Milestone 1 is done when all of the following hold. Each is checkable.

1. **LibKa0s** ships one kit revision (`Kit.VERSION = 8`) carrying `Kit.skip`, `testkit/vendor_sync.lua`,
   `Loader.xmlFiles`, `Kit.assertSuiteInventory`, `Kit.assertSurfaceParity`, the millisecond/clamped
   durations, and the checkpoint-qualified `RESULTS.md` lead-in — with `docs/api/testkit/version-8-docs.md`
   written and `tests/test_kitsync.lua` green.
2. `git ls-files -s testkit/run-automated-tests.sh` and `git ls-files -s tests/_kit/run-automated-tests.sh`
   both report **`100755`** in LibKa0s, and a kitsync case asserts it.
3. `LibKa0s/tests/run.lua` derives its library list from `LibKa0s.xml` and pins its suite list in both
   directions; `lua5.1 tests/run.lua` is green.
4. **LibKa0s is tagged `v1.8.0`** (`M1-LK-14`): `git tag --points-at HEAD` shows it,
   `lua5.1 tests/test_versioning.lua` is green, `CHANGELOG.md` carries the version block, an API document
   exists for every moved minor, `docs/test-cases.md` is regenerated, and the provenance template and repo
   semver both read v1.8.0. **Nothing in Milestone 3 can start before this.**
5. **WowAddonStandards** is at **v2.22.0** with a changelog entry naming every section touched;
   `performance` carries §12; `anti-patterns` runs to #56; `ADDONS.md` carries a library-repo table;
   `toc-file-§5` states that the within-section file sequence is illustrative.
6. **`AUDIT.md:91`** carries the impact-graded severity form and the one-root/derived-dependents rule
   (`M1-STD-17`), so `agents/standards-audit.md`'s new grading rule is not overridden by the fetched
   playbook.
7. **wow-addon** commands and agents carry the ten edits.
8. **No addon repository has been touched *by an M1 item*.** Milestone 2's changes to seven addon
   repositories (ConsumableMaster, PanelMaster, prettychat, WhatGroup, KickCD, LootHistory, BankLedger) run
   in parallel with Milestone 1 by design and are verified against M2's own criteria, not this one.
