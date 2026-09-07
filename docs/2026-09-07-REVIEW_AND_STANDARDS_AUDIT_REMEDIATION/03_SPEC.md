# 03 — Spec

**The normative end state, per cluster. What "done" looks like — never when it happens.**

> **Nothing in this bundle has been executed.** No repository has changed. No tag has been cut, no
> payload copied, no section amended, no `.pkgmeta` line added. Every sentence below is written in the
> imperative because it describes a *target*, not because anything has reached it. Where this document
> says a file "carries" something, read it as "must carry when the cluster is closed".

Inputs: `01_CONSOLIDATED_FINDINGS.md` (207 triaged findings in 39 clusters) and `02_UPSTREAM_CHANGES.md`
(the upstream item list). Ordering, dependencies and effort live in `04_EXECUTION_PLAN.md` and are
deliberately absent here.

---

## How to read this

Every cluster carries three things and nothing else.

- **Target** — the shape that must exist when the cluster is closed.
- **Acceptance** — a check a reader can run or a state a reader can look at, without asking the author
  what was meant.
- **Non-goals** — what this cluster deliberately does not fix, so nobody widens it in flight.

RFC-2119 words carry their usual force. Where this spec and
`WowAddonStandards/standards/STANDARDS.md` (v2.38.0, 2026-09-02) disagree, the standard wins — except in
the ten clusters whose whole point is that the standard is what changes, where the amendment is specified
in `02_UPSTREAM_CHANGES.md` and this document describes the post-amendment state.

**The two gates, once.** A **commit** is gated on `luacheck .` plus `lua tests/run.lua` and nothing
else. A **tag** is gated on all four suites at `pass` in the run's `manifest.json` plus
`suites.complexity.warnings == 0` — no function above CCN 15 — read by `/wow-addon:bump-version`, where a
`skip` blocks as NOT EVALUATED rather than reading as a pass. Nine clusters below name one of these two;
none names a third.

---

## The surfaces this spec depends on, and the version each arrives in

Every cluster whose end state needs something out of LibKa0s names it here rather than describing it in
prose. **All nine consumers sit on `v1.25.0` today** — every root `CLAUDE.md` provenance line says so,
`git diff v1.25.0 HEAD -- LibKa0s/` is empty, and `Kit.VERSION` is 14 at `tests/_kit/framework.lua:20` in
all nine. That flat baseline is a precondition of the table, not a coincidence of it.

| Surface | Where | Today, at v1.25.0 | End state | Arrives in |
|---|---|---|---|---|
| The three composed media rows | `LibKa0s/OptionsCompose.lua:231`, `:275`, `:304` | `COMPOSE_MINOR = 2` (`:29`); each row wraps `O.LSMValues` in a second closure | `COMPOSE_MINOR = 3`; each row assigns `O.LSMValues(kind)` directly | **v1.26.0** |
| `lib.__AttachCompose`'s host contract | `LibKa0s/OptionsCompose.lua:181` | A host-supplied `O.LSMValues` may return a table or a function; both happen to work | A host-supplied `O.LSMValues` **MUST** return a function; documented and pinned by a case | **v1.26.0** |
| `TabStrip` frame acquisition | `LibKa0s/OptionsWidgets.lua:1050-1072`, `:942`, `:643`, `:874-880` | `WIDGETS_MINOR = 13` (`:15`); creates every button and the content panel per click | `WIDGETS_MINOR = 14`; acquires from `LibKa0s-Pool-1.0` | **v1.26.0** if ready, else v1.27.0 |
| `lib.__PatchLSM30Border()` | new, on `LibKa0s-Options-1.0` | absent — no `RegisterWidgetType` anywhere in `LibKa0s/*.lua` | present, lib-level, idempotent behind `lib.__lsmBorderPatched`; Options `MINOR` (`Options.lua:24`) 14 → 15 | **v1.27.0** |
| `lib.STRINGS.DEAD_BUTTON` | `LibKa0s/OptionsCompose.lua:393-402`, `OptionsWidgets.lua:1313-1319` | absent; a handler-less composed reset button renders live and silent | present; reported once at build time from `makeBtn` | **v1.27.0** |
| `Kit.assertSurfaceParity(stub, majorName)` + a machine-readable member manifest | `testkit/framework.lua`, `docs/api/` | absent; nine stubs hand-maintained | present; `Kit.VERSION` 14 → 15 | **v1.27.0** |
| `SetAtlas(name, useAtlasSize)` and `f:__setGeom(w, h)` | `testkit/mock_base.lua` | no `SetAtlas` at all; `f:GetHeight()` returns 0 for every frame (`:97`) | both present and **additive**; `GetHeight` still defaults to 0 | **v1.27.0**, kit 15 |
| `GetHeight` answers recorded geometry | `testkit/mock_base.lua:97` | returns 0 | returns the recorded height | a later tag, **kit 16** |
| The EOL gate | `LibKa0s/tests/test_eol.lua:29` → `testkit/` | scoped to `docs/automated-tests` by its `BUNDLES` constant; lives outside the vendored kit | reads the whole `git ls-files` set; vendored, so all nine inherit it | **v1.27.0**, kit 15 |
| `O.SetRenderer(ctx, fn)` | `LibKa0s/Options.lua:695`, refusal inline at `:700-716` | **published and vendored already** | unchanged — the work is adoption | — |
| `O.BuildLandingPage(ctx, spec)` | `LibKa0s/OptionsWidgets.lua:1288`, `OnRelease` at `:323` | **published and vendored already** | unchanged — the work is adoption | — |
| `lib.ICONS` / `lib.Icon` | `LibKa0s/Media.lua:92`, `:202` | **published and vendored already** | unchanged; the `minimise` key does **not** move | — |
| `LibKa0s-Pool-1.0` | `LibKa0s/Pool.lua:49`, minor 3 | published; four consumers use it, the library itself does not | unchanged; the library becomes its own consumer | — |
| `lib.MakeCloseButton(parent, onClick, addonName)` | `LibKa0s/Core.lua:234` | three arguments | **unchanged. The signature does not move in this plan.** | — |
| `O.MASTER_GROUP` | `LibKa0s/OptionsCompose.lua:189` | published on the instance by `__AttachCompose` | unchanged — one addon-side line | — |

Six rows of that table are surfaces that already exist and are merely unadopted. A cluster that depends
on one of them **depends on no tag**, and any plan that puts it behind a release is wrong. `C07` is the
sharpest case: `O.BuildLandingPage` has been in the payload PrettyChat vendors since before v1.25.0.

---

## Collection-wide invariants

These hold at every point, including mid-cluster.

1. **All four suites stay green in every repository at every committed point.** `luacheck .` at 0/0 and
   `lua tests/run.lua` at 0 failed. Where a new gate is expected to redden a repo — the `M1-LK-01`
   composer cases, the widened EOL gate at `M1-LK-10`, the parity factory at `M4-09` — **the reddening
   is seen, and no commit leaves the repository red**: the gate and its fix land in the same commit, or
   the repair lands first where it produces no commit of its own, as `M1-LK-00`'s `rm` plus
   `git checkout --` does for `M1-LK-10`. Splitting a gate and its fix into two *work items* is fine and
   is how `M1-LK-01` → `M1-LK-02` is deliberately ordered, so the four cases are watched failing before
   `OptionsCompose.lua` is touched; splitting them into two *commits* is what this invariant forbids.
   Item ids throughout this document are `04_EXECUTION_PLAN.md`'s, which `05_TRACEABILITY.md` § 7a
   declares canonical.
2. **`libs/LibKa0s/` and `tests/_kit/` are never patched in place.** They are whole-folder vendored
   payloads. A defect there is fixed upstream, tagged, and re-vendored.
3. **The payload, the kit and the provenance line move in one commit.** `docs/releasing.md:131-137`
   copies both trees and each consumer's `tests/test_vendor_sync.lua` gates both against the single tag
   its `CLAUDE.md` provenance line names. Bumping the line without copying, or copying one tree without
   the other, reddens that gate in the repo that did it.
4. **A minor bump is not complete without its API document.** `tests/test_versioning.lua:165-185` derives
   `docs/api/<Major>/version-<key>-docs.md` from the live `lib.MODULES` table and stays red until the
   file exists. Every minor named in the surfaces table above therefore carries its document in the same
   change as the code. This is enforced, not remembered.
5. **Frozen bundles are evidence and are never edited.** `docs/audits/<date>/`, `docs/reviews/<date>/`
   and `docs/automated-tests/<stamp>/`. Their stale counts, their British spellings and their absent
   `ANALYSIS.md` files stay exactly as recorded. Anything written into a bundle stamped months ago is a
   fabricated record, which is why `C08`'s end state is forward-only.
6. **US English in authored prose and player-facing strings**, with two standing exemptions: Blizzard and
   third-party symbols reproduced verbatim, and the `minimise` key in `lib.ICONS`, which is a public
   catalog key from which `lib.Icon` derives a path to `minimise.tga` on disk in ten vendored trees.
7. **Every count claim names its members.** A bare "seven files" or "nine stubs" is the shape that goes
   stale silently; three of this cycle's findings are exactly that. Where this spec states a count it
   either lists the members or names the command that produced it.

---

# Part A — the upstream end state

Sixteen clusters whose resolution is a change to LibKa0s, to the standard, or to both. Four of them
resolve by **reversing a disposition**: the work the ledger assigns to ten repositories is not work those
repositories should do.

---

## C01 + CX01 — a composed media row hands the flow engine a table-returner

**Target.** `FontGroup`, `BorderGroup` and `BarGroup` declare `values = O.LSMValues("font")`,
`("border")` and `("statusbar")` — the closure `O.LSMValues` (`LibKa0s/Options.lua:764`) already returns,
assigned once at row-declaration time. `enumList` (`LibKa0s/OptionsWidgets.lua:78-79`) unwraps it once
and gets a table. `COMPOSE_MINOR` reads 3; the Options version key moves `14.13.2.3` → `14.13.3.3` and
`docs/api/Options/version-14.13.3.3-docs.md` exists.

`lib.__AttachCompose`'s docstring states the contract the change creates: a host that supplies its own
`O.LSMValues` **MUST** return a function, because the composer now calls the member once at file load
rather than at each dropdown render. Today a table-returner works by accident, and **MultiMeters ships
one** — `settings/Schema.lua:670` reads `C.LSMValues = function(t) return lsmValues(t)() end`. In the end
state that line reads `C.LSMValues = lsmValues`.

The three private workarounds are gone, because each was written against this defect and each names its
own end condition: AbsorbTracker's `LSM_KIND` and `fixMediaValues` (`settings/Appearance.lua:114-137`)
with its three call sites at `:181`, `:237`, `:257`; ConsumableMaster's `lsmValues`
(`settings/MacroBar.lua:121-123`) with its three row overrides at `:269`, `:337`, `:454`; MultiMeters'
one line. LibKa0s issue #15, named in ConsumableMaster's comment at `:118`, is closed.

KickCD's eight composed rows populate in game with **no KickCD code change at all** —
`settings/Castbar.lua:346`, `:481`, `:503`, `:514`, `:536`, `settings/Icons.lua:207`, `:258`,
`settings/Label.lua:184`. It is the only consumer whose visible behaviour changes on the re-vendor alone,
which is what makes it the proof.

**Acceptance.**
- `grep -c 'function() return O.LSMValues' LibKa0s/LibKa0s/OptionsCompose.lua` → `0`;
  `grep -c 'values = O.LSMValues' LibKa0s/LibKa0s/OptionsCompose.lua` → `3`.
- `tests/test_options_compose.lua` carries four cases: three asserting
  `type(rows[n].values()) == "table"` and non-empty for the three groups, and one asserting a
  host-supplied table-returning `LSMValues` is rejected. **All four are seen red before the composer is
  touched.** A case that has only ever been green is not a gate.
- `grep -rn 'fixMediaValues\|LSM_KIND' AbsorbTracker/settings/` returns nothing;
  `grep -n 'lsmValues' ConsumableMaster/settings/MacroBar.lua` returns nothing;
  `grep -n 'C.LSMValues' MultiMeters/settings/Schema.lua` returns exactly `C.LSMValues = lsmValues`.
- In client, with the fixed payload loaded: `/kcd config` shows Icons, Label and Castbar font, border and
  bar-texture dropdowns listing real media names; `/dump LibStub("LibKa0s-Options-1.0").MODULES.OptionsCompose`
  reports `3`.
- LibKa0s issue #15 is closed, citing the tag.

**Non-goals.** Adding any new library surface — the fix deletes a closure, it does not publish one.
Changing what `O.LSMValues` returns; its deferral is load-bearing and its own docstring at `:759-763`
says why. Making `enumList` tolerate a doubly-wrapped value, which would hide the next instance of this
instead of catching it. Touching the `row.values == nil` guard at `OptionsWidgets.lua:1442`, which is
correct — it is the double wrap that made the row non-nil and empty.

---

## C02 — a widget-type re-registration is a library concern

**Target.** `LibKa0s-Options-1.0` publishes `lib.__PatchLSM30Border()` at Options `MINOR` 15: lib-level
rather than per-instance, idempotent behind `lib.__lsmBorderPatched`, so five vendored copies of the
library in one session register the widget once. Each of the five addons calls it from the live arm of
`settings/OptionsSetup.lua`, and the five private `core/LSMPatch.lua` files are deleted — AbsorbTracker
50 lines, ConsumableMaster 65, PanelMaster 66, KickCD 68, MultiMeters 101, five distinct md5s.

The standard carries the rule the finding had nothing to cite: a widget-type re-registration against
AceGUI's process-global registry is a LibKa0s concern and never a per-addon one, plus an anti-pattern
(the list ends at #75) naming the process-global tell. `anti-patterns` #8 continues to sanction
`RegisterWidgetType` extension over forking — the new rule is about *where* the registration lives, not
whether extension is legitimate.

**Acceptance.**
- `ls */core/LSMPatch.lua` across the collection returns nothing.
- `grep -rn 'RegisterWidgetType' <repo>/core <repo>/modules <repo>/settings` returns nothing in any of
  the ten repositories; the only hits anywhere are under `libs/`.
- `grep -n '__lsmBorderPatched' LibKa0s/LibKa0s/Options.lua` resolves, and a headless case calls
  `lib.__PatchLSM30Border()` twice asserting the second call is a no-op.
- **In client, all five loaded together**: each addon's Border dropdown draws the same styled control,
  and the styling does not depend on load order. This cannot be proved headless — the failure mode is
  "whichever addon loaded last owns everyone's dropdown" — so the in-client check is the acceptance
  criterion, not a supplement to it.

**Non-goals.** Forking `LSM30_Border`. Changing the wrapper's appearance. Deleting the five copies before
the promoted surface has been seen working with all five still present. AbsorbTracker's copy is the one
real divergence — it exposes a callable `NS.ApplyLSMBorderPatch()` at `core/LSMPatch.lua:20` invoked from
`core/AbsorbTracker.lua:52` rather than a `PLAYER_LOGIN` frame — so it is the last deleted, not the first.

---

## C09 — the shared runner records what it measured

**Target.** `testkit/run-automated-tests.sh` at `Kit.VERSION` 15 gets four things right that it gets
wrong today.

The pass regex at `:195` spans the skipped count. `framework.lua:566` prints
`N passed, N failed, N skipped, N total`; the regex today is
`'[0-9]+ passed, [0-9]+ failed(, [0-9]+ total)?'`, so `awk '{print $5}'` reads empty and `TESTS_TOTAL`
falls back to `passed + failed` — a skipped case reads as a pass. The manifest's `tests` object carries a
`skipped` key. The trend row at `:388` renders `version → release` when `manifest.release` is set, rather
than `$ADDON_VERSION` alone, which is why `LibKa0s/docs/automated-tests/RESULTS.md:16` records Version
1.24.0 for a bundle whose manifest says `"release": "1.25.0"`. And the corrected four-checkpoint lead-in
at `:414-432` reaches an **existing** `RESULTS.md`: today it sits in the branch taken only when the file
is absent or its header mismatches, so not one of the ten repositories can ever receive it.

**Acceptance.**
- A suite containing one deliberately skipped case, run through
  `tests/_kit/run-automated-tests.sh --no-bundle`, prints a non-zero skipped figure and a total that
  includes it.
- The newest bundle's `manifest.json` has `suites.tests.skipped`.
- A release run's `RESULTS.md` row shows both versions in the Version cell.
- All ten `RESULTS.md` files carry the four-checkpoint lead-in with every existing row preserved.
- `grep -h 'Kit.VERSION' */tests/_kit/framework.lua | sort -u` returns one line reading 15.

**Non-goals.** Making `perf` or `complexity` gate a run or a commit. Hand-editing any `RESULTS.md`
figure — every number in that file is written by the runner, and a hand-edit is the defect `C08` is
about. Changing the column names, which ten files' history depends on.

---

## C12 — the shared mock can express a geometry assertion

**Target, in two kit revisions, because this is not additive.** `testkit/mock_base.lua:97` answers
`GetHeight` with 0 for every frame and defines no `SetAtlas` at all, so
`OptionsWidgets.lua:433-442`'s atlas-derived tab pitch always takes its `L.TAB_H` fallback and any
`options-ui-§13` invariance assertion passes vacuously. Four repositories filed the missing case; none of
them can write one.

- **Kit 15 is purely additive.** `SetAtlas(name, useAtlasSize)` writes a height from a kit-published
  atlas table, and `f:__setGeom(w, h)` is an opt-in. `GetHeight` still defaults to 0. All nine
  consumers take kit 15 and nothing moves.
- **Kit 16 flips the default**, once each consumer has adopted the opt-in where it needs geometry.

Roughly 308 test files across ten repositories lean on geometry answering zero. Shipping both revisions
at once is the version of this that reddens nine suites simultaneously for a fortnight.

**What covers the interval, because something has to.** The same tab strip is being rewritten inside this
plan: `C23`'s change makes tab buttons and the content panel pooled and re-dressed, in a widget the live
settings code of all nine addons renders. Its only headless proof is a `CreateFrame` count, and the case
that would catch a stale label or a moved band is exactly the one kit 15 cannot express. Until kit 16, the
witness is an operator: `06_SMOKE_TESTS.md` § 3.5 cycles every multi-tab panel in all nine after the
`M4-01` wave. That is a weaker check than the four findings ask for, and it is named here rather than
left as an unstated gap between two clusters.

**Acceptance.**
- Kit 15: `grep -n 'function f:SetAtlas\|__setGeom' tests/_kit/mock_base.lua` resolves in all nine, and
  every repository's pass count is **unchanged** from its pre-adoption figure. An unchanged count is the
  whole acceptance criterion for an additive mock change.
- Kit 16: each repository that wants one carries a case asserting the chrome band height and every row's
  y offset are identical across each tab selection, and that case is **verified red** under a mutation to
  the tab atlas heights.

**Non-goals.** Flipping `GetHeight` in kit 15. Rewriting any repository's `tests/wow_mock.lua` to work
around the kit — the kit is where the fidelity contract lives.

---

## CX02 — the nine degradation stubs are checked, not hand-maintained

**Target.** `testkit/framework.lua` publishes `Kit.assertSurfaceParity(stub, majorName)` at kit 15,
against a machine-readable member manifest under `docs/api/`. All nine addons carry a
`tests/test_surface_parity.lua` calling it; today only AbsorbTracker, ConsumableMaster and KickCD carry
one at all, which is how AbsorbTracker's stub omits `SetRenderer` outright with every suite green.

The nine stubs stay hand-written — `settings/OptionsSetup.lua` in each, MultiMeters 384 lines,
AbsorbTracker 369, KickCD 351, PrettyChat 265, WhatGroup 258, BankLedger 230, PanelMaster 217,
LootHistory 199, ConsumableMaster 185. What changes is that a divergence between a stub and the live
surface goes red instead of shipping.

**The library does not publish a no-op surface, and this is not a compromise.** A published no-op would
have to live in the payload that is *by definition absent* on the path the stub exists for:
`AbsorbTracker/settings/OptionsSetup.lua:44` opens `local lib = LibStub and LibStub("LibKa0s-Options-1.0", true)`
and the stub is the arm below it. A library cannot ship the thing that stands in for its own absence.

**Acceptance.**
- `grep -n 'assertSurfaceParity' tests/_kit/framework.lua` resolves in all nine.
- Each of the nine has `tests/test_surface_parity.lua`, and deleting one member from that repo's stub
  turns it red.
- AbsorbTracker's stub publishes `SetRenderer`, and its parity case is red without it.

**Non-goals.** Publishing a no-op module from LibKa0s. Generating the nine stubs. Unifying their
line counts — a stub mirrors what its host consumes, and nine hosts consume different subsets.

---

## C23 — the tab strip acquires frames instead of creating them

**Target.** `TabStrip` (`LibKa0s/OptionsWidgets.lua:1050-1072`) acquires its buttons and its content
panel from per-`ctx` `LibKa0s-Pool-1.0` pools rather than calling `CreateFrame` through `makeTab`
(`:942`) and `drawContentPanel` (`:643`) on every click while `releaseLedger` (`:874-880`) only hides and
reparents. `makeTab` splits into `newTabButton` and `dressTab`, with `OnClick` re-set on each dress.
`WIDGETS_MINOR` reads 14. Internal to the library; no surface moves.

The library ships `LibKa0s-Pool-1.0` at minor 3 (`Pool.lua:49`) and is the one repository in the
collection that does not use it — BankLedger, KickCD, LootHistory and MultiMeters all do.

**Acceptance.**
- `grep -n 'LibKa0s-Pool-1.0' LibKa0s/LibKa0s/OptionsWidgets.lua` resolves.
- A headless case selecting each tab twice asserts that the second pass creates **no** new frames,
  counted through the mock's `CreateFrame`. It is red against today's code.
- Every existing `test_options_widgets.lua` case stays green: this is a lifetime change, not a
  behavioural one.

**Non-goals.** Unifying the library's three release contracts in one change — `Widgets.lua:799-825`'s
hand-rolled handle/box pool is correct as it stands, and `LIBKA0S-R-05` is the duplication behind `C23`,
not a second defect. Pooling anything outside the tab strip.

---

## C24 — the options and perf seams stop swallowing their own diagnostics

**Target.** Four library-local defects, one end state.

`lib.STRINGS.DEAD_BUTTON` exists, and `makeBtn` (`OptionsWidgets.lua:1313-1319`) reports once at build
time when a composed button has no handler, then renders anyway — the shape `EMPTY_DROPDOWN`
(`:1443`) already sets. The composer builds `resetAll` and `resetPosition` unconditionally
(`OptionsCompose.lua:393-402`), so **every host that does not pass `onResetAll` newly prints**; the nine
specs are audited in the same wave, so the report lands on real gaps rather than on nine addons at once.

`OptionsWidgets.lua:696`'s `local print = d.print or function() end` is replaced by the shell's
constructed sink, stored as `O.__print` and read by `__AttachWidgets`. `Options.lua:289-291` already has
the type guard and the `DEFAULT_CHAT_FRAME` fallback; the widget printer having neither is part of why
`C01` shipped in silence.

`Perf.lua:478` reuses bracket slots from a high-water free list rather than allocating
`{ key = key, t0 = debugprofilestop() }` per bracket in the capture arm, its docstring states the
active-arm cost, and a case measures the active arm beside the dormant one at
`tests/test_perf_isolation.lua:66`. `Perf.lua:615-618` takes `C_SpecializationInfo.GetSpecialization`
before the bare global, modelled on the `C_AddOns` shim at `Env.lua:60-66`.

**Acceptance.**
- `grep -n 'DEAD_BUTTON' LibKa0s/LibKa0s/OptionsWidgets.lua LibKa0s/LibKa0s/OptionsCompose.lua` resolves,
  and a case asserts a handler-less composed button reports exactly once.
- Opening each of the nine addons' settings panels after adoption prints no `DEAD_BUTTON` line. A line
  that does appear names a real missing handler and is fixed, not silenced.
- `grep -n 'O.__print' LibKa0s/LibKa0s/OptionsWidgets.lua` resolves; a case asserts `NO_GROUPS` reaches
  the shell's sink.
- `tests/test_perf_isolation.lua` carries an active-arm allocation case with a stated ceiling derived
  from three runs.

**Non-goals.** Making the widget printer a public surface. Changing what `Perf` measures. Raising
`DEAD_BUTTON` to an error — the precedent is report-and-render.

---

## C10 — line endings become a gate instead of a recurring sweep

**Target.** Two halves, and the smaller one comes first.

**Upstream.** Seven tracked LibKa0s files are LF in the working tree under `attr text=auto eol=crlf`:
`LibKa0s/DebugLog.lua`, `LibKa0s/Pool.lua`, `tests/test_debuglog.lua`, `tests/test_pool.lua` and three
`docs/api/` documents. **All seven are repaired before the gate is widened**, not two of them — the
widened gate reads the working tree, so leaving five behind turns the library's own suite red with no
item to fix it. The first two are the only stragglers in the collection that sit inside a **shipped**
payload, and with PrettyChat's vendored copies of the same two files, which are LF today and therefore
the one consumer whose byte diff currently passes, they are four paths carrying one defect. They make
`docs/releasing.md:135`'s byte check — `diff -r LibKa0s <Addon>/libs/LibKa0s`, SHOULD be empty —
report roughly 2,000 phantom lines in nine repositories on every re-vendor, forever. The index is already
correct; only the working tree is wrong. `tests/_kit/vendor_sync.lua` passes because it strips CR against
the git blob, which is why nobody has chased it.

The EOL gate reads the whole tracked set and lives in the vendored kit. `LibKa0s/tests/test_eol.lua:29`
sets `BUNDLES = "docs/automated-tests"` and scans nothing else, which is how the library's own payload
files escaped it. `line-endings-§7` cites that gate rather than only supplying a command, and
`line-endings-§5` sanctions a clearly delimited appendix block below the canonical `.gitattributes` body
for repo-specific extension-less binaries — PanelMaster's `tools/artwork/bin/realesrgan-ncnn-vulkan`
(`.gitattributes:70`) is currently caught between `§4`'s "mark every binary type" MUST and `§5`'s
"byte-for-byte one of two canonical bodies" MUST, and its `docs/ARCHITECTURE.md:197` says so.

**Per repository.** `git ls-files --eol` reports zero `w/lf` or `w/mixed` files under
`attr eol=crlf`, excluding the `tests/_kit/*.sh` carve-out, which is correctly `eol=lf`. The index needs
no change anywhere, and **that is exactly why `git add --renormalize .` is the wrong tool**: it rewrites
an index that is already correct and leaves the working tree as it found it, which is why nothing has
ever reported these. The repair is `rm <path> && git checkout -- <path>` per file — what
`tests/test_eol.lua`'s own failure message tells you to run.

The counts the ledger carries are not the counts to work from. Re-enumerated today over
`git ls-files --eol | grep -E 'w/(lf|mixed)'` minus the `attr eol=lf` scripts: MultiMeters 21,
LootHistory 9, KickCD 8, ConsumableMaster 7, LibKa0s 7, PanelMaster 6, WhatGroup 6, BankLedger 4,
PrettyChat 4 and AbsorbTracker 2. PrettyChat is 4 rather than the 2 `PRETTYCHAT-A-07` recorded because
that finding scoped itself outside `libs/`, and the two it left out are `libs/LibKa0s/DebugLog.lua` and
`libs/LibKa0s/Pool.lua` — the shipped payload. Both statements are true against their own scope; the
finding's scope is the one that hides the two that matter.

**Acceptance.**
- In LibKa0s: `git ls-files --eol | grep -E 'w/(lf|mixed)'` returns only the two `.sh` files under
  `attr eol=lf` — all seven repaired, and repaired **before** the gate widens.
- `diff -r LibKa0s <Addon>/libs/LibKa0s` is byte-empty for every re-vendored consumer. This check has
  never passed in this collection; when it does, it is the acceptance criterion.
- The EOL suite is present in `tests/_kit/` in all nine and reads `git ls-files`; converting one tracked
  file to LF turns it red.
- `line-endings.md` carries the appendix sanction, and PanelMaster's `.gitattributes` and its register
  row agree.

**Non-goals.** Renormalising the index. Touching frozen bundle files whose line endings are part of what
was frozen — the sweep is scoped to the tracked live tree, and each repository states which frozen paths
it excluded.

---

## C16 — the documentation map gets its fourth table

**Target.** `documentation.md:279` MUSTs every `.md` under `docs/` appear in **exactly one** of three
tier tables, and seven documents belong to no tier — `testing.md`, `smoke-tests.md` and the five
verification-and-record docs, which `§3` itself places outside the tier model at `documentation.md:56-62`.
The rule as written is unsatisfiable, and **all nine addons independently wrote the same workaround**: a
`### Verification and record` table at `AbsorbTracker` `docs/ARCHITECTURE.md:332`, BankLedger `:199`,
ConsumableMaster `:287`, KickCD `:204`, LootHistory `:360`, MultiMeters `:660`, PanelMaster `:148`,
PrettyChat `:190`, WhatGroup `:320`.

In the end state `§3` names that fourth table and settles whether `ARCHITECTURE.md` registers itself.
Nine repositories then comply by doing nothing, and `PRETTYCHAT-A-09` and `WHATGROUP-A-15` close as
correct-as-written rather than as defects.

**Acceptance.**
- `documentation.md` names a fourth table and states the self-registration rule.
- A fresh `/wow-addon:standards-audit` in any of the nine files no `documentation-§3` row about the
  fourth table.
- The ripple is swept: `NEW_ADDON.md:204`, `NEW_ADDON_CONTEXT.md:1299`,
  `wow-addon/commands/sync-docs.md:12`, `wow-addon/CLAUDE.md:50`,
  `wow-addon/agents/standards-audit.md:40`. `AUDIT.md:96` already says "exactly one table" and needs
  nothing.

**Non-goals.** Moving any document between tiers. Deleting the nine existing tables — they are the
answer, and the amendment ratifies them.

---

## C25 — the standard and the library stop being out of date about each other

**Target.** `LibKa0s/LibKa0s/LibKa0s.xml` lists fourteen `Script` entries — Core, Env, Pool, Item, Media,
Widgets, DebugLog, Slash, Options, OptionsWidgets, OptionsCompose, OptionsScroll, Perf, PerfPanel. The
standard says thirteen files in three places (`STANDARDS.md:57`, `library-stack.md:70`,
`open-evolutions.md:13`) and the Options row at `library-stack.md:82` lists only `Options.lua`,
`OptionsWidgets.lua`, `OptionsScroll.lua`. The missing file is **`OptionsCompose.lua`** — the file where
`C01` lives. The document describing the module set does not know the file that broke nine addons'
dropdowns exists.

In the other direction, LibKa0s `CLAUDE.md:3` and `README.md:3` both point at standard v2.28.0 against a
live v2.38.0, and the `options-ui-§15`–`§18` sections `OptionsCompose.lua` cites arrived at v2.38.0.

**Acceptance.**
- `grep -rn 'thirteen files' WowAddonStandards/` returns nothing;
  `grep -n 'OptionsCompose' WowAddonStandards/standards/standards/library-stack.md` resolves.
- LibKa0s's two pointers read the standard version the rollup lands as, and `docs/releasing.md` carries a
  pointer check in its step order so this moves on a schedule rather than on an audit.

**Non-goals.** Auditing the rest of the standard's prose against the library file by file. `LIBKA0S-R-14`
(OptionsScroll) was wrong — `OptionsScroll.lua` **is** in the table — and does not come back.

---

## C22 — the 1500-LOC cap says what it binds

**Target.** `layout.md:55` caps "any single `.lua` file" while `layout-§1`'s scope is the source
skeleton — its block lists `tests/` at `:39`, and `:52`'s MUST names only `core/`, `defaults/`,
`settings/`, `locales/` and `modules/` as where source lives, so a test file is inside the picture and
outside the rule in the same section. The cap is undefined in three directions, and
the collection answers differently in each repository: ConsumableMaster filed
`CONSUMABLEMASTER-A-06` against a test file, MultiMeters filed none of its six test breaches, PrettyChat
registered a deviation at `docs/ARCHITECTURE.md:221` asking for "a layout revision that sanctions a
generated-data folder", and LibKa0s held `LIBKA0S-A-03` at low precisely because nothing says whether the
cap binds a library repo.

In the end state `layout-§1` states whether the cap binds `tests/`, whether it binds generated
non-shipping data, and `library-stack-§7` carries the applicability list it is missing. Its block at
`library-stack.md:175-179` promises "three lists below" and delivers two applicability lists —
"Applies, unchanged" at `:182-193` and "Does not apply" at `:195-209` — plus a *Substitutes* list at
`:211-228` that answers a different question. Between them the two applicability lists omit layout,
architecture, performance, compat, anti-patterns, public-api, debug-logging, events-frames-taint,
standalone-windows, naming-cheatsheet, audit-review-history and `documentation-§4` entirely.

**The census is 18 files, not the eleven `C22` states, and two of its five named repositories have
none.** KickCD's largest source file is `modules/Castbar.lua` at 1320 and PanelMaster's largest tracked
file is `tests/test_artwork.lua` at 1356 — their findings are complexity-band and on-notice items, not
cap breaches. What is over cap: MultiMeters seven source files (`settings/Schema.lua` 3069,
`modules/Tooltip.lua` 2652, `modules/Window.lua` 2644, `modules/Aggregator.lua` 2058,
`modules/Export.lua` 1743, `core/Diagnostics.lua` 1726, `modules/Row.lua` 1702) and seven test files
(`tests/test_window.lua` 2737, `test_tooltip.lua` 2708, `wow_mock.lua` 2265, `test_row.lua` 1606,
`test_aggregator.lua` 1605, `test_schema.lua` 1573, `test_export.lua` 1509);
`ConsumableMaster/tests/test_macrobar.lua` 1894; `LibKa0s/LibKa0s/OptionsWidgets.lua` 1838 and
`tests/test_options_widgets.lua` 2287; `PrettyChat/GlobalStrings/GlobalStrings.lua` 23,842.

**The cluster's other half is complexity, and it blocks two release gates.** `automated-tests.md:143`
gates a tag on `suites.complexity.warnings == 0`, and two repositories cannot pass it today: KickCD has
one — the CCN-18 anonymous function at `tests/test_schema.lua:595-631`, whose own comment at `:613` names
the seam (`KICKCD-R-02`) — and MultiMeters has **23**, every one of them in shipped `core/`, `modules/`
or `settings/` source, topping out at `scanColumn@1439-1540` in `modules/Aggregator.lua` at **CCN 36**.
Neither is a cap breach and neither belongs to the ruling above, but both sit in this cluster because the
question is the same one: what the standard's size rules bind, and what a repository does about a number
they leave standing.

**Acceptance.**
- `layout.md` states the `tests/` and generated-data scope; `library-stack.md` carries the missing
  applicability list naming every section the first two omit.
- `PanelMaster/settings/PanelEditor.lua` (1350) has a disposition: it crossed its **own** recorded split
  trigger, which reads "if the next change also grows it, execute the split rather than re-accept".
- Every file still over the cap after the ruling either has an open issue naming the seam or a register
  row with a re-check trigger. Nothing sits over the cap unremarked.
- KickCD reports **zero** complexity warnings, so its release gate is passable.
- Every one of MultiMeters' 23 warnings carries a disposition — split, accepted with a register row and a
  re-check trigger, or an open issue naming the seam — and `scanColumn` has a decision either way,
  because the `C04` work edits inside it.

**Non-goals.** Splitting MultiMeters' seven source files, or any of its 23 warned functions: the
deliverable there is the disposition, not the split. Splitting `GlobalStrings.lua`, which is
generated, unloaded and `.pkgmeta`-ignored and must be exempted by rule. Any split before the ruling —
most of `C22` may not be a breach at all.

---

## CX04 — the TOC MUST is measured against the right denominator

**Target.** `toc-file-§5:144` binds narrowly: "A line whose position is load-bearing MUST carry a comment
saying so… naming what resolves at load". `CX04` counted annotations against all 23–81 lines of nine TOC
files and concluded the MUST is unworkable. Measured against what it actually says, this is roughly
**eight one-line additions**, and `AbsorbTracker.toc:39-40` is already a fully compliant instance.

The end state is those eight lines — `KICKCD-A-02` names two positions (`KickCD.toc:55`, `:73`),
`PRETTYCHAT-A-01` two (`PrettyChat.toc:40`, `:57`, after correctly dropping a third), `WHATGROUP-A-02`
four (`WhatGroup.toc:44`, `:47`, `:53-56`) — plus a settled reading of `toc-file-§5:147`'s *conventional*
SHOULD, once per group, which is what is genuinely near-universally unmet. `AbsorbTracker.toc:36-37` is
the only instance of that SHOULD anywhere in the collection. A SHOULD being unmet does not make the MUST
wrong.

**Acceptance.**
- Each of the eight named positions carries an at-line comment naming the symbol and its publisher, in
  the shape `AbsorbTracker.toc:39-40` uses.
- A fresh audit against any of the nine files no per-line `toc-file-§5` MUST row.
- `toc-file.md` states whether the conventional SHOULD is per group or per line.

**Non-goals.** Annotating 23 to 81 lines in nine files. Rewriting the MUST — it is correct as written and
the disposition is what was wrong.

---

## CX05 — lint covers the test tree, and the standard's template says so

**Target.** `lint.md:11` ships
`exclude_files = { "libs/", "docs/audits/", "docs/reviews/", "_dev/", "tests/" }` as the template and
`lint.md:32` states it normatively: "`tests/` is excluded from lint (the harness is exercised by running
it, not by linting it)". All ten repositories comply **exactly**. The underlying observation is real —
302 tracked source `.lua` against 308 tracked `tests/*.lua` outside `tests/_kit/`, so a clean-lint claim
covers about half the collection's Lua — but as dispositioned it asks ten repositories to violate the
standard's own template.

In the end state the template narrows the exclusion to `tests/_kit/` and adds a `files["tests/"]` stanza
declaring the kit globals, `LibKa0s/.luacheckrc:4` proves that shape first, and the other nine follow.
`luacheck .` is 0/0 in ten repositories with the test tree in scope.

**Acceptance.**
- `grep -n 'tests/_kit/' <repo>/.luacheckrc` resolves in all ten and no `.luacheckrc` excludes bare
  `tests/`.
- `luacheck .` reports 0 warnings / 0 errors in all ten with the tests linted.
- `WHATGROUP-A-14`'s separate gap closes in the same shape: `.luacheckrc` and `.pkgmeta` agree about
  `_dev/`.

**Non-goals.** Turning 308 test files on at once behind a blanket ignore, which is worse than the
exclusion because it reads as coverage and provides none. Linting `tests/_kit/`, which is genuinely
redundant with `testkit/` in the library.

---

## CX06 — `MakeCloseButton` keeps its signature, and the declines are ratified

**Target.** `lib.MakeCloseButton(parent, onClick, addonName)` (`LibKa0s/Core.lua:234`) **does not
change**. Eight addons publish a three-line currying wrapper and that is the correct shape: the third
argument is the addon folder name, the library is vendored, and `LibKa0s/Media.lua:14-20` records that
`...` carries the folder name only for a file the TOC loads directly — so the library cannot infer it.
Rebinding saves roughly 24 lines and costs a signature change to a surface all nine consumers vendor.

What changes is the record and the rule. `standalone-windows.md:30` MUSTs that every close control an
addon builds be built through the wrapper, while `:34` says a host MAY draw a different one on its own
windows. Those cannot both hold, and `BankLedger/core/CoreSetup.lua:117-129` is defective on sight under
one and compliant under the other. The section resolves the contradiction so that a reasoned decline is a
terminal compliant state, and BankLedger carries one register row citing it with a re-check trigger.

**The ledger's decline count is one release stale and the correction is part of the end state.**
LootHistory has **adopted** — `core/CoreSetup.lua:167` wraps `lib.MakeCloseButton` with `addonName`, and
its comment at `:19-25` records that the old decline "expired with LibKa0s v1.10". BankLedger is the only
decline in the collection.

**Acceptance.**
- `grep -n 'function lib.MakeCloseButton' LibKa0s/LibKa0s/Core.lua` still reports three parameters.
- `standalone-windows.md` states the terminal compliant state; BankLedger's `docs/ARCHITECTURE.md`
  register carries the row; a fresh audit files no MUST row against BankLedger's four title bars.
- No document in the collection still says LootHistory declined.

**Non-goals.** `lib.SetHost(addonName)` or any other rebinding. Changing BankLedger's four visible close
controls, which would be a player-visible change with no player benefit.

---

## C17 — the spelling gate reads the section's list

**Target.** `localization-§5` names its own enforcement as review plus `/wow-addon:standards-audit` and
supplies a Use/Never prose table rather than a machine-readable list. LibKa0s built a gate anyway, and it
is `BRITISH = { "colour", "grey", "behaviour", "synthesise", "normalis", "recognis" }`
(`tests/test_prose.lua:113`) — six substrings, two of which are not in `§5`'s table at all. It stays green
while `minimise` ships as a public `lib.ICONS` key (`Media.lua:94`) and `CANCELLED` reaches chat text a
player reads at `Perf.lua:723`, `:864`, `:948`, `:1029`, `:1063`. A gate that reads as coverage and
provides none is `testing-§12`'s exact failure mode, sitting inside the gate for `§5`.

In the end state `§5` publishes the canonical substring list its own table implies and requires a
mechanical gate to use it **whole**; LibKa0s's gate reads that list; and the authored prose in
ConsumableMaster (25 live sites), KickCD (37 hits in 11 live files), WhatGroup (three comments) and
LibKa0s is swept.

**The `minimise` key does not move.** `lib.Icon` (`Media.lua:207`) builds the path *from* the key and the
file on disk is `minimise.tga`, vendored into all nine `libs/LibKa0s/media/icons/` trees. Adding
`"minimize"` to `lib.ICONS` alone yields a path to a file that does not exist — the silent failure
`Media.lua:190-196` itself records, where a texture that fails to load draws nothing and raises nothing.
Live consumers are `MultiMeters/modules/HeaderControls.lua:127` and `core/Diagnostics.lua:333`. The key
stays, and LibKa0s's register carries a row saying why.

**Acceptance.**
- `localization.md` carries the substring list; `tests/test_prose.lua`'s list is that list, not a second
  private one.
- The gate is red against today's `Perf.lua` strings and green after the sweep.
- `grep -rniE 'colour|behaviour|grey' <repo> --exclude-dir=libs --exclude-dir=_kit --exclude-dir=audits --exclude-dir=reviews --exclude-dir=automated-tests`
  returns nothing in the four repositories.
- `lib.ICONS` still carries `minimise`, and LibKa0s's register says so.

**Non-goals.** Renaming a public catalog key for a spelling. Editing frozen bundles, whose spellings are
part of the record. Sweeping vendored `libs/`.

---

# Part B — the addon end state

Twenty-three clusters that are repository-local. Six of them depend on nothing upstream at all and are
marked as such, because scheduling them behind a library release is the most likely way this plan goes
wrong.

---

## C03 — a migration runner is gated on the scope it writes

**Depends on nothing upstream.**

**Target.** Two addons, one root cause, and the highest blast radius in the plan because a wrong fix
corrupts a real ledger.

BankLedger ships `schemaVersion = NS.SCHEMA_VERSION` in `defaults/Global.lua:14`, so
`core/Database.lua:17`'s `g.schemaVersion = g.schemaVersion or 1` always reads the current version and
the `< NS.SCHEMA_VERSION` arm at `:21` never runs against a real pre-stamp store. In the end state the
key is not an AceDB default: `RunMigrations` seeds it, and an empty ledger is what separates a fresh
install from a pre-stamp store.

ConsumableMaster's `core/Database.lua:65-90` reads and stamps `g.schemaVersion` — account-wide — while
both migration steps write `db.profile`. The `OnProfileChanged` hook at
`core/ConsumableMaster.lua:401-410` therefore does nothing on a second profile. In the end state
profile-writing steps gate on `db.profile.schemaVersion` and account-wide steps stay on `db.global`.

**Both defects are pinned by tests that cannot go red, so the fakes are fixed first.**
`BankLedger/tests/wow_mock.lua:582-589` returns `deepcopy(defaults.global)`, so setting the key nil reads
nil — it does not model AceDB's default fallback, and neither does the kit fake.
`ConsumableMaster/tests/test_database.lua:56-63` is named "never writes into the profile scope" while both
steps write `db.profile`, and its second assertion pins the very account-wide key the defect is.

**Acceptance.**
- BankLedger: a case with `schemaVersion` absent and one `vendorPrice` row runs the v1→v2 arm. It is red
  against today's `defaults/Global.lua`.
- ConsumableMaster: a multi-profile case switches profile and asserts the profile-scoped step ran. It is
  red today.
- `tests/wow_mock.lua` models the AceDB default fallback — metatable or logout strip — and the absent-key
  case is written against it. **No assertion is weakened to make a case pass.**
- In client, on a copy: back up SavedVariables, hand-edit to drop `schemaVersion` and add a
  `vendorPrice` row, log in, expect the `v1 -> v2, 1 rows touched` debug line, log out, confirm the stamp
  persisted. For ConsumableMaster, create and switch to a second profile and confirm the migration line
  fires — today it does not.

**Non-goals.** Changing either addon's `SCHEMA_VERSION`. Migrating anything the current steps do not
already migrate. Writing to a live SavedVariables file during verification.

---

## C04 — the feign trace costs nothing when it is disarmed

**Depends on nothing upstream. Entirely inside MultiMeters.**

**Target.** `modules/Aggregator.lua:1488-1496` reads a plain published boolean before building anything,
and the read is hoisted above the per-source loop — today `judge` sits inside
`for index, src in ipairs(column.sources)` and `modules/Feign.lua:102-105` builds a fields table and its
nested order table *before* `TraceFeign`'s nil check, so a disarmed trace allocates two tables per Deaths
source per refresh. `Diagnostics.IsFeignTraceArmed` (`core/Diagnostics.lua:1618`), which has no production
caller today, reads that same published field.

The ring stops evicting the lines it exists to show: `judge` is admitted only for GUIDs a cast line named,
with a suppressed-row counter, or each kind gets its own bounded ring —
`FEIGN_TRACE_MAX = 120` at `core/Diagnostics.lua:1604` with `table.remove(log, 1)` at `:1643` currently
lets `judge`, which fires per death row per refresh, evict them. The `O(n)` shift at `:1643` becomes a
write index into a fixed table.

The eviction branch that most likely explains issue #25 emits a trace: `modules/Feign.lua:247-249`'s
`if unit == nil then feigned[guid] = nil` falls through with no trace call, and `:280` reports
post-eviction state so `noted` and `down` both read `<evicted>`. `settings/Slash.lua:470-484` names a
rejected argument instead of printing a report — today `/mm debug of` prints a report and leaves the
trace armed.

**Acceptance.**
- A perf scenario measures a Deaths refresh with the trace disarmed and asserts zero allocation
  attributable to the trace. Red against today's code.
- Cases cover: the `judge` admission boundary; a cast line surviving a full ring; the not-in-group
  eviction emitting its own verdict; `noted` and `down` distinguishable after eviction. Each names what
  it is red under.
- `/mm debug of` prints a rejection naming the argument, and `/mm debug feign` still reports.
- `tests/perf.lua:564`'s `PROBE_OFF_BYTES_CEILING` is re-derived from three runs after the change, with
  the measured figure and the date in the comment. It reads 336000 against a commented 325955 and a
  measured 310158.1 today.

**Non-goals.** Splitting `core/Diagnostics.lua` (1726) or any other over-cap file in this repository —
that is `C22`, deferred, and it collides head-on with this cluster. Triaging issue #25 itself; this
cluster gives it a trace, it does not close it.

---

## C05 — a byte estimate counts every field it declares

**Depends on nothing upstream.**

**Target.** `LootHistory/core/Database.lua:748-754` sums its seven string fields inline rather than
walking a literal array with `ipairs`, which runs zero iterations for a currency record built without an
`itemLink` (`modules/Collector.lua:190-196`) and charges flat overhead instead. The per-record allocation
`LOOTHISTORY-R-04` named disappears with the same two lines.

`tests/test_database.lua:379` asserts an exact byte total over a fully populated fixture plus a currency
row, not `s.bytes > 0` — which passes today at 512 bytes of pure overhead, over fixture rows that carry no
zone and therefore already run the truncating path.

**Acceptance.**
- The case asserts an exact total and carries a `-- red under:` comment naming the walk. It is red
  against today's `estimateRecordBytes`.
- A currency record with no `itemLink` estimates more than the flat overhead.

**Non-goals.** Changing what the storage-stats panel displays. Making the estimate exact against real
SavedVariables serialisation.

---

## C06 — a stored chat format is checked against its conversion signature

**Depends on nothing upstream.**

**Target.** PrettyChat's `Schema.Set` (`settings/Schema.lua:464`) refuses a write whose conversion
sequence differs from the shipped default's. `conversionSequence` moves into `modules/Override.lua` as
`NS.ConversionSequence`, so the Preview and the writer read one implementation. Today `row.set` stores
any string and `buildSampleArgs` (`modules/Override.lua:275-292`) synthesises arguments from the format
itself, so `RenderSample` can never see a surplus conversion — the Preview reports success and the raise
happens later, inside Blizzard's chat handler, on every matching message.

**Acceptance.**
- Setting a player format with a surplus `%s` is refused with a message naming the mismatch, and the
  Preview agrees with the writer.
- `tests/test_defaults.lua` asserts an override's conversion sequence is a positional **prefix** of
  Blizzard's — never longer, never type-mismatched at a position — rather than equality.
- In client: enter a format with an extra conversion, confirm the refusal; enter a valid one, confirm a
  matching message renders.

**Non-goals.** Validating anything about the format beyond its conversion signature. Changing any shipped
default.

---

## C07 — the landing page is the library's renderer

**Depends on nothing upstream. `O.BuildLandingPage` is already in the v1.25.0 payload PrettyChat
vendors — this cluster does not wait on any tag.**

**Target.** `PrettyChat/settings/Panel.lua:646-721` is replaced by a call to
`H.BuildLandingPage(ctx, spec)`, and `settings/OptionsSetup.lua`'s degradation stub publishes a
`BuildLandingPage` no-op. The library's renderer (`LibKa0s/OptionsWidgets.lua:1288`) sets, at `:323`, the
`OnRelease` that hides the logo texture; PrettyChat's hand-copy caches `pcLogo` and sets no `OnRelease`
at all, so a 300px logo survives into whatever widget next takes AceGUI's pooled `SimpleGroup` — and that
pool is shared with every other addon in the session.

**Acceptance.**
- `grep -n 'buildParentBody' PrettyChat/settings/Panel.lua` returns nothing; `BuildLandingPage` resolves.
- The parity case covers `BuildLandingPage` on the stub arm.
- In client: open PrettyChat's landing page, page to another addon's settings, confirm no logo rides
  through. This is the acceptance criterion — the leak crosses addons and no headless case sees it.

**Non-goals.** Changing the landing page's artwork or copy. Fixing AceGUI's pooling.

---

## CX03 — the sidebar combat guard is where the pages are

**Depends on nothing upstream. `O.SetRenderer` is published at `LibKa0s/Options.lua:695`.**

**Target.** `O.SetRenderer` owns the Blizzard-sidebar combat refusal, inline at `Options.lua:700-716`.
AbsorbTracker has **zero** callers outside `libs/` and drives three pages off raw
`ctx.panel:SetScript("OnShow", …)` — `settings/Appearance.lua:320`, `General.lua:283`,
`Profiles.lua:57` — while its own `docs/settings-panel.md:278-285` documents the refusal it therefore
does not deliver. KickCD keeps Profiles and Spells off it; MultiMeters keeps Profiles off it.

In the end state those pages route through the helper, drop their own `EnsureDefaultsButton` call, and
**`SetRenderer` is published by each repository's degradation stub in the same commit** — AbsorbTracker's
stub omits the member entirely today, which is why nothing went red.

**Acceptance.**
- `grep -rn 'SetScript("OnShow"' <repo>/settings/` returns nothing that renders a settings page.
- Each repository's `settings/OptionsSetup.lua` stub publishes `SetRenderer`, and its parity case is red
  without it.
- In client, **in combat**: open each addon from the Blizzard AddOns sidebar and expect the refusal
  message and a closed panel. This is the point of the cluster and it cannot be proved headless.

**Non-goals.** Moving pages that are already on `SetRenderer`. Changing the refusal's wording, which is
the library's.

---

## C29 — state is read at the moment it is used

**Target.** Seven findings across four repositories, one shape: a value read once and used later, or a
gate evaluated once and never re-evaluated.

`WhatGroup/modules/Frame.lua:148-151` re-evaluates visibility on a combat transition, registered
symmetrically for `PLAYER_REGEN_DISABLED`/`ENABLED` — hide when the gate closes, show when it opens with
`pendingInfo`. Today `ApplyFrameVisibility` only hides and nothing drives it across the transition.
`core/WhatGroup.lua:605`'s `autoShow` read moves inside the scheduled callback, which already re-reads
`pendingInfo` for exactly this reason. `core/WhatGroup.lua:678` keys captures by `searchResultID`
resolved through the existing `GetApplicationInfo` bridge, rather than binding
`table.remove(captureQueue, 1)` to whatever application id arrives, and declined and cancelled
applications clear `pendingApplications`.

`BankLedger/settings/Slash.lua:92-103`'s `ResetEverything` sends `Ka0s_BankLedger_SettingsChanged` once at
the end, so the Ledger's capture gate (`modules/Ledger.lua:872-878`) re-caches instead of staying stale
until reload. `KickCD/modules/Castbar_Debug.lua:42` prints its secret branch unconditionally, with
`C_CurveUtil` availability as a separate clause rather than a wrapper with no `else`.

**Acceptance.**
- WhatGroup: a case entering and leaving combat with the gate closed and then open asserts the frame
  follows. Red today.
- WhatGroup: a case with two outstanding applications asserts the capture pairs to the right one.
- BankLedger: a case asserts `ResetEverything` broadcasts once; the Ledger's cached gate is observed to
  update.
- In client, WhatGroup: enter combat with the frame shown, confirm it hides; leave combat with a pending
  invite, confirm it returns.

**Non-goals.** Re-architecting WhatGroup's application flow. Adding a message bus where direct calls are
already correct.

---

## C30 — the settings panels take the shape `options-ui` describes

**Target.** Eight findings, five of them repository-local shape and three of them waiting on a ruling.

Local: `PanelMaster/settings/PanelEditor.lua`'s five page acts — Copy `:607`, Enabled `:633`, Unlock
`:648`, Reset `:667`, Delete `:673`, all currently inside `sections[TAB_GENERAL]` — move into the
`H.PageHeader` band drawn at `:1112-1199`, the emptied General tab goes, the `:1058` fallback re-points,
and `docs/settings-panel.md:257`'s paragraph arguing the current placement is rewritten in the same
commit. `ConsumableMaster/settings/Panel.lua:866-867` defers `Settings.RegisterAddOnCategory` on
`InCombatLockdown` and retries from the existing `PLAYER_REGEN_ENABLED` handler rather than registering
from a `PLAYER_LOGIN`/`ADDON_LOADED` bootstrap (`:984-993`) with no guard.
`LootHistory/settings/Slash.lua:178-181` subtracts `config` from the degraded help list, so the degraded
path stops offering a verb that then declines. `WhatGroup/settings/Panel.lua:285` keys off
`Helpers.MASTER_GROUP` rather than the hand-typed `["Master controls"]` copy of
`OptionsCompose.lua:50`, and `:207` passes the `addonName` upvalue the file already binds at `:14`.

Waiting on a ruling: `PanelMaster`'s three hand-written border and bar control groups
(`settings/PanelEditor.lua:738-757`, `:770-800`, `:814-830`) edit registry records, and no composer arm
fits a record-backed bind — either the composers gain one or the repository carries an `options-ui-§16`
register row. `MultiMeters/settings/Schema.lua:1553-1566`'s two All-surfaces broadcast meta rows are
misclassified by `options-ui-§16`'s grep, which is an upstream narrowing.

**Acceptance.**
- PanelMaster: the five acts render in the chrome band; `docs/settings-panel.md` agrees with the code.
- ConsumableMaster: an in-combat `/reload` does not register the category, and the existing regen handler
  does. Verified in client — this is a taint-adjacent path and the headless suite cannot see it.
- LootHistory: on a library-less load, `/lh help` does not list `config`.
- WhatGroup: `grep -n '"Master controls"' settings/Panel.lua` returns nothing.
- Each remaining hand-written group either composes or has a register row with a re-check trigger.

**Non-goals.** Redesigning any page. Composing PanelMaster's record-backed groups before the composer can
express them.

---

## C28 — a stored value is validated before it reaches an API

**Target.** Eight findings, one shape.

`AbsorbTracker`'s `NS.GetThrottleWindow` sits beside the three getters that already clamp
(`GetMasterAlpha:248`, `GetMasterScale:257`, `GetBarAlpha:276`) and `modules/Timer.lua:50` calls it rather
than passing a raw `GetSetting` into AceTimer. `core/Units.lua:111-119`'s `CopyFromPlayer` routes its
nineteen appearance keys and the mirror flag through `NS.SetByPath`, so the write seam logs them.

`ConsumableMaster` has one `colorDecode` returning nil for an absent channel, shared by
`settings/OptionsSetup.lua:101-104` and `settings/Slash.lua:295-298`, which today disagree — `or 1`
against `or 0` — with the per-surface default staying in `KCM.SwatchColor`.
`KickCD/settings/Panel_Render.lua:304` early-returns when the defaults tree is absent rather than carrying
a `y = -180` fallback contradicting `defaults/Profile.lua:314`'s 120.
`PanelMaster/core/Util.lua:99-106` treats a shorthand alpha of `<= 1` as already fractional under
byte-scale RGB, so `"255,0,0,1"` no longer yields an invisible panel at alpha 0.0039;
`modules/Registry.lua:588`'s `DeleteAll` clears `NS.State.preview` through the same private sweep
`dropSessionIDs` uses at `:561`. `PrettyChat/core/PrettyChat.lua:20-25` builds a fresh merged table
instead of mutating `NS.ProfileDefaults` in place, and `modules/Override.lua:154` tracks global presence
in a separate key set so a global absent from this client is restored to nil on disable.

**Acceptance.**
- Each of the eight has a case that is red against today's code, named in the case's own comment.
- `PanelMaster`'s round-trip colour cases cover the mixed-scale input.
- `grep -n 'ProfileDefaults' PrettyChat/core/PrettyChat.lua` shows no in-place assignment.

**Non-goals.** Clamping every stored number in the collection. Changing any default value.

---

## C27 — an allocation nit is fixed only where it is measured, and a ceiling bounds something

**Target.** Two halves, and the second is the one that matters.

The ceilings bound what the suite measures. `AbsorbTracker/tests/perf.lua:235`'s
`PROBE_OFF_BYTES_CEILING = 320` cites a 312.0 baseline against a measured 48.0 bytes per iteration — 6.7×
the value it guards. `MultiMeters/tests/perf.lua:564` reads 336000 commented "measured 325955" against a
measured 310158.1, so the stated 3.5% headroom is 7.7%. Both are re-derived from three runs with the
figure and the date recorded, after `C04` lands in MultiMeters' case.

The allocation nits are taken **only with a scenario that measures them**, and skipped otherwise.
`KickCD/modules/Castbar.lua:833` allocates a closure per cast start and there is no `castStart` scenario;
`LootHistory/modules/AuctionPrice.lua:58,73` rebuilds a settings-invariant provider map per kept loot
line, dwarfed by the pcall'd cross-addon fetches on the same line;
`ConsumableMaster/settings/Panel.lua:908-928` allocates a closure and a timer per `RequestRefresh` call,
roughly 150 during one first-open item-info burst; `PanelMaster/modules/Canvas.lua:642-666` never clears
its mouseover `OnUpdate` script, and its comment at `:654-656` claims it "stops doing any work the moment
the tracked set is empty", which is false. **The false comment is the larger defect in that last one**,
and correcting it is not optional even if the driver stays.
`AbsorbTracker/modules/Display.lua:375` passes its open bucket as `Perf.Note`'s third argument, as
`appearance:236` and `visibility:320` already do.

**Acceptance.**
- Each re-baselined ceiling carries its measured figure, its margin and the date, and is derived from
  three runs rather than one.
- Every allocation change has a perf scenario that measures it, added **first**. A change with no
  scenario is not made.
- `PanelMaster/modules/Canvas.lua:654-656` describes what the code does.

**Non-goals.** Chasing allocations on event-rate paths with no measurement. Adding scenarios for their
own sake.

---

## C26 — a ratified exemption reproduces its own evidence

**Target.** Each `performance-§12` exemption page's sweep reproduces today. The exemptions survive on
merit in all four repositories; their evidence does not.

`LootHistory/docs/performance.md:40-60` claims eleven events against thirteen registered
(`modules/Browser.lua:1277-1278` is missing) and four timers against five (`core/ItemSetup.lua:71`,
`core/Util.lua:242`, `settings/OptionsSetup.lua:181`), and cites `Compat.lua:202` and
`OptionsSetup.lua:129`, neither of which exists. Its `CHAT_MSG_LOOT` row at `:45` says "one table insert"
where `modules/Collector.lua:123-124` runs `GetItemExtras` — a `C_TooltipInfo` build via
`Compat.ScanBound` — and then `GatherAll`'s three-addon cascade; that row is the one claim bearing on
criterion (a)'s substance, so it is rewritten to name the tooltip build and the price cascade and to
re-affirm (a) explicitly rather than by omission.

`PrettyChat/docs/performance.md:33-50` asserts zero `C_Timer` calls in `settings/`; the page's own grep
now returns `settings/Panel.lua:528`, `:531`, `:532`, and the one-shot `C_Timer.After(0)` gets a
render-path disposition. `BankLedger/docs/performance.md:39` repoints from `core/Compat.lua` to
`core/ItemSetup.lua:67`, where the `C_Timer.After(0.4, cb)` actually is.
`WhatGroup/modules/Frame.lua:275` arms its cooldown ticker only when the frame is shown, and the
register row claiming the ticker "cannot outlive that window" is amended to match.

**Acceptance.**
- Running each page's own greps verbatim reproduces the tables printed on the page.
- Every `file:line` on each page resolves.
- No exemption is withdrawn — each still names criterion (a) plus (b) or (c).

**Non-goals.** Re-litigating any exemption. Adding the perf harness to an exempt addon.

---

## C11 — the release zip carries what a player needs and nothing else

**Depends on nothing upstream for the four real omissions.**

**Target.** Nine `.pkgmeta` ignore blocks stop diverging — and the end state separates two things the
audits ran together, because only one of them is player bytes.

**Player bytes, measured.** `media/screenshots` is tracked in every repository that has one and ignored in
only three (`ConsumableMaster`, `PanelMaster`, `PrettyChat`, plus `BankLedger`), so four addons ship it:
**KickCD 7.5M, LootHistory 5.9M, AbsorbTracker 2.0M, WhatGroup 880K — 16.3M in total**, downloaded by
every player of those four for art that is served from the project page. WhatGroup additionally ships
`CLAUDE.md` and `DEPENDENCIES.md`, keeping `README.md` and `LICENSE`, which players do read. This is the
half of `C11` that changes what a player downloads, and no audit in this cycle named it.

**Not player bytes, and listed anyway.** `.claude`, `.superpowers` and `.pytest_cache` are **untracked in
every repository in the collection** — `git ls-files` returns nothing for any of them anywhere, and
`AbsorbTracker/.gitignore:11,15` ignores both by name — so a packager clone receives none of them and no
`.pkgmeta` line changes a single downloaded byte. AbsorbTracker's `.superpowers` is 2.8M across 60 files
on disk, 30 of them `review-*.diff`, and reaches nobody. They still belong on the ignore lists, because
`packaging.md:28`'s strong form MUSTs that every root dotfile and dot-directory **present in the repo**
either appear there or be justified beside it, tracked or not; the check is about a list going stale, not
about a package growing. Recording which half a line belongs to is the point: the same evidence was used
to *reject* `BANKLEDGER-A-03`, `MULTIMETERS-A-04` and `WHATGROUP-A-13` in Part 3 of
`01_CONSOLIDATED_FINDINGS.md`, and it has to mean the same thing in both directions.

`packaging.md`'s own minimum template (`:9-24`) gains `.pkgmeta`, because it lists `.luacheckrc`,
`.gitignore`, `.gitattributes`, `.claude`, `.superpowers`, `docs`, `tests`, `_dev` and `*.bak` but not
`.pkgmeta` itself — while `packaging.md:28` MUSTs that every root dotfile either appear in the ignore list
or be justified in a comment. Seven repositories followed the template and are non-compliant for it; only
ConsumableMaster and MultiMeters ignore `.pkgmeta` today. The `.claude`/`.superpowers` half of the
template is already there at `:18-19`, so the self-reference is the whole edit.

**Acceptance.**
- `git ls-files` in each repository, filtered through that repository's own `.pkgmeta` `ignore:` list,
  returns no `media/screenshots/`, no `CLAUDE.md` and no `DEPENDENCIES.md`. **There is no packager
  dry-run to run**: no repository carries `.github/workflows` and `packaging.md:32` puts CI out of scope,
  so the tracked set against the ignore list is the only check that exists.
- Every root dot-entry in each repository either appears in that repository's `ignore:` list or carries a
  one-line justification comment beside it, and each entry for an untracked directory says so, so the
  next reader does not re-file it as shipping.
- `packaging.md`'s template names `.pkgmeta`.

**Non-goals.** A shared `.pkgmeta` — nine addons ship different trees. Ignoring `README.md` or `LICENSE`.

---

## C13 — the perf panel draws its own close button

**Target.** AbsorbTracker's `core/PerfSetup.lua:149-159` and KickCD's `:217-226` delete their `decorate`
field. `LibKa0s/PerfPanel.lua:191-196` draws the identical control anchor for anchor, and the descriptor
already supplies what the library needs — AbsorbTracker names `addonName` at `PerfSetup.lua:43`, KickCD
carries `name = addonName` at `:69`, which feeds the library's `d.addonName or d.name`. MultiMeters'
equivalent hook goes the same way.

**Acceptance.**
- `grep -n 'decorate' <repo>/core/PerfSetup.lua` returns nothing in the three repositories.
- A case asserts the descriptor carries `addonName` and no `decorate`.
- In client: `/at perf`, `/kcd perf`, `/mm perf` each open a panel with one close button in the same
  place as before.

**Non-goals.** Changing the perf panel's chrome. Removing the `decorate` seam from the library.

---

## C31 — naming, lint config and vendored-payload hygiene

**Target.** Eight small items with no shared mechanism beyond being config and naming.

`AbsorbTracker/libs/LibStub/` holds exactly what `AbsorbTracker.toc:17` loads — `LibStub.lua` — with
`tests/` and `LibStub.toc` gone. `KickCD`'s bare WoW globals take the `_G.` prefix its own files already
use in the same place (`modules/IconGrid.lua:232` beside `:148`, `modules/Cooldowns.lua:80`,
`settings/Panel_Widgets.lua:121` and three more), and `modules/Castbar_Debug.lua`'s eight signatures
rename their `print` parameter to `emit`, matching `settings/Slash.lua:61`'s `out(line)`.
`ConsumableMaster`'s three `KCM.Debug` sites (`settings/Category.lua:764`, `modules/Selector.lua:610`,
`:655`) use `%s`, per `docs/debug.md:30`'s ban on `%d`/`%f` on the secret-safe sink; the rendered line is
identical because `SafeToString` already ran. `LootHistory` pins `NS.version`
(`core/Namespace.lua:5`) against `## Version:` in the TOC with a case that parses the TOC, rather than
asserting equality only on the branch where the TOC is unreadable. `WhatGroup`'s `.luacheckrc` and
`.pkgmeta` agree about `_dev/`.

**Acceptance.**
- `find <repo>/libs/LibStub -type f` lists exactly the file the TOC loads.
- `grep -rnE '^\s*(UnitClass|UnitExists|GetTime)\(' KickCD/modules KickCD/settings` returns nothing
  unprefixed.
- Editing the TOC version without editing `core/Namespace.lua` turns LootHistory's suite red.

**Non-goals.** A collection-wide `_G.` sweep — only KickCD was verified. Renaming anything a player sees.

---

## C18 — user-facing text goes through the `L` seam

**Target.** Four repositories, and the coverage test that cannot see the gap.

`ConsumableMaster`'s two custom widgets take `local L = KCM.L` and wrap their six literals —
`modules/KCMMacroDragIcon.lua:74`, `:77`, `modules/KCMItemRow.lua:171`, `:173`, `:175`, `:228` — with
colour escapes kept outside the key. `KickCD`'s three cast-bar desc keys used at
`settings/Castbar.lua:219`, `:227`, `:302` are defined in `locales/enUS.lua` with the current sentences,
and the three superseded keys go; today the `__index` at `locales/enUS.lua:15` returns the key, so enUS
renders correctly and only a translator would see the gap. `LootHistory`'s two localized-text scanners
(`core/Compat.lua:229`, `modules/Attribution.lua:66-67`) match `[ \194\160]` rather than `%s`, so a
surviving NBSP does not break the exact `WARBAND_LINES` lookup. `PrettyChat`'s `settings/Slash.lua` usage
lines at `:241`, `:278-284`, `:349`, `:365`, `:379` are either wrapped or recorded as known residue, and
`docs/ARCHITECTURE.md:228`'s register row stops claiming an unwrapped string is detectable.

**The coverage test changes shape, in every repository that has one.** `tests/test_locale.lua:44-50`
builds its call-site list from a `gmatch` of `L["…"]`, so it can only find strings that are already
wrapped. A coverage case that scans for wrapped strings and calls the result coverage is
`testing-§12`'s failure mode. The end state derives the candidate set from the TOC-derived source list
and reports unwrapped literals.

**Acceptance.**
- Each repository's locale coverage case is red when a new bare literal is added to a settings file.
- `KickCD`: every desc key used resolves in `locales/enUS.lua`; a TOC-derived `L[…]` coverage case is
  seen red first.
- No register row claims detection the suite does not perform.

**Non-goals.** Adding a second locale. Translating anything.

---

## C19 — a comment's named file, line or caller exists

**Target.** Roughly forty sites across seven repositories where a comment names a function, a line or a
hazard that has moved or gone. The house style carries `file:line` citations and design arguments in
prose and nothing verifies them, so they rot silently.

The end state cites the **symbol** wherever the name is unambiguous and re-derives the genuinely
positional citations against the tree. Named instances:
`ConsumableMaster` eight of fourteen citations (`core/DebugLogSetup.lua:93`, `:113`,
`modules/MacroBarButton.lua:115`, `:146`, `tests/test_surface_parity.lua:84`, `:126`);
`AbsorbTracker/core/Units.lua:74` and `:108` say fifteen appearance keys where `APPEARANCE_KEYS` holds
nineteen and the header at `:19` says nineteen; `AbsorbTracker/core/AbsorbTracker.lua:69` cites a
`CreateOptionsPanel` re-entrancy hazard the library now owns at `Options.lua:838-844`;
`LootHistory/defaults/Global.lua:6-9` says the v1→v2 migration bumps the stamp to 2 where the suite
asserts 8, and `core/Database.lua:195` says "v6->v9" where there is no v9;
`LootHistory/modules/Browser.lua:1162` describes a gap `:1074-1077`'s `OnHide` hook already covers;
`PanelMaster/settings/OptionsSetup.lua:190-195` names `Sl:CliResetAll`, which no file defines;
`BankLedger/settings/OptionsSetup.lua:180-181` says `MasterControls` is reached via `ComposeMaster` on an
arm that returns at `:214`; `MultiMeters/tests/test_vendor_sync.lua:14` quotes v1.8.3 against a live
v1.25.0; `PrettyChat/tests/test_vendor_sync.lua:25` quotes v1.10.2 the same way.

**Acceptance.**
- Every `file:line` in a comment in the live tree resolves, checked by the sweep
  `wow-addon/commands/sync-docs.md` gains for exactly this.
- `AbsorbTracker/core/Units.lua` states nineteen or states nothing and lets `APPEARANCE_KEYS` answer.
- No vendor-sync comment quotes a version the provenance line does not carry.

**Non-goals.** Deleting the citation style — it is what makes these files readable, and the answer is a
check, not fewer citations. Touching comments in frozen bundles or in `libs/`.

---

## C20 — an exported symbol has a caller or a stated reason

**Target.** Seams published for a caller that never arrived either go, or are recorded as deliberate.

Gone: `AbsorbTracker/settings/Schema.lua:101-111`'s `NS.PartitionUnitRows`, whose only caller is its own
test at `tests/test_schema.lua:524-530`, with its case and its `docs/test-cases.md` entry;
`KickCD/tests/test_bus.lua:48`'s pre-`KCD-09` `NewBusTarget` fallback branch;
`KickCD/modules/Castbar_Debug.lua:125`'s `or _G.print` arm, which `core/CoreSetup.lua:112` and `:171`
make unreachable, together with the now-spent note at `docs/ARCHITECTURE.md:278-284`;
`ConsumableMaster/tests/test_surface_parity.lua:169-174`'s duplicated paragraph.
`AbsorbTracker/core/Database.lua:95-112`'s `migrateAllProfiles` reduces to
`forEachProfile(NS.MigrateProfileToV3)` rather than hand-copying the walk and its four-line comment block.

Recorded rather than deleted: `PrettyChat`'s three published-but-uncalled seams —
`core/MediaSetup.lua:62`'s `NS.Icon`, `core/CoreSetup.lua:111`'s `NS.MakeCloseButton` and `:78`/`:132`'s
`NS.Format` — each of which is argued in place. Their intent goes into `docs/module-map.md` so a later
dead-code sweep does not misread them. `PrettyChat`'s degradation stub publishes a nil-returning
`MakeCloseButton` so the two arms stop being asymmetric, and `coreSurface` names it.
`ConsumableMaster/tests/test_surface_parity.lua:44-52` adds `MakeCloseButton` to `CORE_SEAM` with a
`CORE_LIVE_ONLY` entry recording its deliberate deadness.

**Acceptance.**
- `grep -rn '<symbol>' <repo> --exclude-dir=docs` returns more than the definition for every remaining
  export, or the export is named in `docs/module-map.md` with its reason.
- Case counts move by exactly the deletions, and each repository's `docs/test-cases.md` and README badge
  move in the same commit.

**Non-goals.** A collection-wide dead-export gate. Deleting a seam whose reason is written down.

---

## C21 — a test can go red

**Target.** Nine cases across six repositories that stay green under the change they exist to catch.

`KickCD/tests/test_schema.lua:581`, `:630` and `tests/test_options_panel.lua:552` restore the shared
instance in a guaranteed-run wrapper or take a fresh `T.load(true)` per case, rather than restoring on the
last line of a body that `tests/_kit/framework.lua:613` pcalls.
`LootHistory/tests/test_database.lua:379` asserts an exact total (`C05`), and an integration case calls
`modules/Attribution.lua:327-361`'s `Enable()` against the mock, asserting the registered event set and
the hooked globals — today it has zero test callers and its seven events, one unit frame and five hooks
are entirely uncovered. `LootHistory/tests/run.lua:43-47`'s lifecycle kick is published through
`Kit.expose` and pinned against `OnInitialize`'s actual call set, which it currently misses by one
(`NS.Slash:Register`). `MultiMeters/tests/test_diagnostics.lua:1373-1381` asserts on the printed roster
lines rather than on `pcall` returning true. `PanelMaster/core/Database.lua:141` calls `NS.Version()`
rather than the `NS.version` constant `tests/test_database.lua:160` asserts, and the mock TOC version
points at a different string so that case can fail. `WhatGroup/tests/run.lua:59-77`'s suite list is pinned
in both directions; `tests/test_mediasetup.lua:147-155` scans `media/` for any `.ttf`/`.otf` and any
filename in the library catalog rather than one hard-coded path; `tests/test_libka0s.lua:806` asserts
`src ~= nil` before the `assertNil`, and derives `SEAM_FILES` from the TOC-derived load list.
`LibKa0s/tests/run.lua:110-118` gains one comment naming `Kit.assertSuiteInventory`
(`testkit/framework.lua`) as what holds its hand-typed suite list honest.

**Acceptance.**
- Every case named above is **seen red** under the mutation its comment names, then green. A case whose
  red has not been observed does not close its finding.
- Renaming a suite file, or dropping one from a runner's list, turns that repository red.

**Non-goals.** Weakening any assertion to make a case pass. Raising case counts for their own sake.

---

## C14 — a ratified deviation lives in one place

**Target.** `docs/ARCHITECTURE.md`'s deviation register is the collection's ratification store, and
nothing verifies it. In the end state every row's cited audit ID resolves in `docs/audits/`, every row's
rule citation resolves in the current standard, and every row's re-check trigger is evaluated rather than
merely readable.

Named rows: `AbsorbTracker`'s three IDs at `:354`, `:356`, `:357` cite `AT-A-10`/`AT-A-03`/`AT-A-09`,
which appear in no bundle — `docs/audits/2026-08-05/` carries `AT-30` through `AT-50`.
`LootHistory:392`'s trigger has fired — upstream `options-ui` now names session-only rows in three
places — and `WhatGroup/docs/ARCHITECTURE.md:349` carries a row whose trigger fired on 2026-08-06 and is
still open. `PrettyChat/docs/ARCHITECTURE.md:222` holds a row for a `toc-file-§5`/`layout-§1` order
conflict that no longer exists: `toc-file.md:109` and `layout.md:53` now state the identical order and
`toc-file.md:109` says so in as many words, while GitHub issue `WowAddonStandards#2` stays open.
`ConsumableMaster:316` cites a rule the standard changed — `toc-file.md:129` now says the TOC comment is
itself compliant. `PanelMaster:199` records a pre-release state contradicted by tag `1.0.0-release`.
`BankLedger` and `LootHistory` each carry an English-only decision argued in a comment and absent from
the register; `LootHistory`'s SetRenderer decline lives only in closed issue #21;
`KickCD:241` holds a provisional row that says of itself it is under review.

`audit-review-history` gains a third MUST: a row's re-check trigger is evaluated against the tree, and a
cited evidence id must resolve. Today `audit-review-history.md:32-39` mandates resolving the rule citation
and nothing else, while `documentation.md:37-40` defines the trigger as something a reader can evaluate
without requiring anyone to.

**Acceptance.**
- A case in each repository asserts every deviation ID cited in `ARCHITECTURE.md` resolves in
  `docs/audits/`.
- No row cites a rule the current standard does not carry.
- No row's trigger has already fired.
- Every decline that lives only in a comment or a closed issue has a row: BankLedger's English-only,
  BankLedger's close button (`CX06`), LootHistory's English-only and its #21.

**Non-goals.** Re-litigating any ratified decision. A register row per finding — the register holds live
ratified deviations, not history.

---

## C15 — the README and ARCHITECTURE structure is the one `documentation-§1`/`§3` names

**Target.** `KickCD/docs/ARCHITECTURE.md` carries `## Overview` and `## Module map` — it is the only
sibling without them, with the material sitting under "What it does", "Subsystems at a glance" and "Load
order" — and its inbound anchors and map row move with the rename.
`LootHistory/README.md:36`'s `## Unreleased` third changelog is promoted into the next bump's
`## What's new` plus a Version History row, and `:141`'s `## Auction-house pricing` folds into
`## How attribution works`. `MultiMeters/docs/ARCHITECTURE.md` (787 lines) spills Known limitations and
Overview to `scope.md`, Taint notes to `midnight-quirks.md` and Event subscriptions to `module-map.md`,
one link each, and its Topic detail table gains one `audits/` row and one `reviews/` row beside
`revendor/`. `PrettyChat/README.md:71-82`'s eight-row per-tab table moves to `docs/settings-panel.md`,
leaving the page-granularity table at `:66-69`, and `CLAUDE.md` gains a one-sentence adherence line above
the Standards compliance heading. `WhatGroup/README.md:121` says Chat, matching `Schema.lua`'s grouping
and `:21`, and its settings table collapses to page granularity.

**Acceptance.**
- Each repository's `docs/ARCHITECTURE.md` carries the mandated section names, and every inbound anchor
  resolves.
- No addon README carries more than the two changelog surfaces `documentation-§1` names.
- Each README settings table is page-granular, with tab detail in `docs/settings-panel.md`.

**Non-goals.** Rewriting content that is already in the right place. Adding a `CHANGELOG.md` to an addon
root, which `documentation-§1` forbids.

---

## C08 — the automated-test record is regenerated, never written

**Target.** Every `RESULTS.md` row, standing section and watch list is produced by
`tests/_kit/run-automated-tests.sh` and describes the tree it measured. Ten repositories are one to eight
runs behind today, and the drift is uniform: AbsorbTracker's newest row reads 508 tests / 7997 NLOC / 29
files / max CCN 14 against 547 / 8903 / 27 / 15 measured; BankLedger 13409/2043/791 against
14174/2153/831; ConsumableMaster 698/58/15870 against 749/59/17632; KickCD prose 756 cases against a table
row of 780 and 841 today; LootHistory 594 "as of 20260807-114650" against a newest row of 644 and 699
today; MultiMeters "0 warnings" against 23 measured, with bands recorded at 1371 and 1232 against 3069 and
2644; PanelMaster 731/11223/1379 against 763/12122/1472; PrettyChat 260 cases over 17 files against 300
over 18; WhatGroup 485/6377 against 528/7047; LibKa0s "499 cases" against 764 and "nothing over the 1500
cap" against a manifest recording `overCapFiles: 2`.

**The record is only writable once the standard stops contradicting itself.** `documentation.md:68` calls
`RESULTS.md` "**generated**, never hand-edited" while `automated-tests.md:222-241` MUSTs a per-entry
disposition and a standing section for each of the other three suites — narrative no generator produces
and the runner writes none of. That contradiction, not addon laziness, is why the record is stale in ten
repositories, and `automated-tests-§3` has no gate reading it.

**Forward-only.** 93 frozen dated bundles carry 35 without an `ANALYSIS.md`, not the ledger's "46 of 89",
and `automated-tests.md:245` only MUSTs one for **release** runs. Writing an analysis today into a bundle
stamped in August fabricates a record. The next run in each repository writes one; the gap is noted once,
in that analysis.

**Acceptance.**
- `automated-tests-§4` and `documentation-§3` agree about what is generated and what is authored, and
  every mandated element of `RESULTS.md` is producible by the runner. **This is a code change, not only a
  ruling**: `testkit/run-automated-tests.sh:388-437` writes one table row plus a fixed lead-in and
  nothing else today — no complexity watch list, no per-suite standing section — so the two things
  `automated-tests.md:221-224` MUSTs have no producer at all. The runner gains them, and the only cell
  left authored is the watch list's **Disposition** column, carried forward by the runner while its entry
  is unchanged.
- In each repository, the newest `RESULTS.md` row's figures equal a fresh run's, and the row count equals
  `ls -d docs/automated-tests/*/ | wc -l`.
- Every watch-list entry resolves against a fresh `lizard` run and carries a disposition.
- No frozen bundle gains a file.

**Non-goals.** Backfilling any `ANALYSIS.md`. Hand-editing any measured figure. Making `RESULTS.md` gate
a commit.

---

## CX07 — a Tier 2 doc exists where its trigger has fired

**Target.** `docs/compat-layer.md` exists in MultiMeters (761 lines of `core/Compat.lua`, 31 shims),
ConsumableMaster (83) and WhatGroup (130 lines, seven shims at `core/Compat.lua:24`, `:40`, `:52`, `:62`,
`:83`, `:105`, `:125`), each covering the shims and their degrade contracts, with the documentation-map
row flipped from Not applicable to Present. `docs/slash-dispatch.md` exists in AbsorbTracker
(`PROFILE_VERBS` at `settings/Slash.lua:327` dispatched at `:386`, 17 verbs in `NS.COMMANDS:60`) and
ConsumableMaster (`settings/Slash.lua:202` reads "seventeen verbs, five sub-command tables"), with
`ARCHITECTURE.md`'s Slash Commands section spilled to a summary plus a link.

`documentation-§3`'s `compat-layer.md` trigger gets a number. `documentation.md:237` reads
"`core/Compat.lua` carries **addon-specific** shims beyond what LibKa0s supplies" — pure judgment, where
`slash-dispatch.md` got "eight or more commands" (`:235`) and `message-bus.md` got "more than ten"
(`:238`). Four repositories read it four ways: BankLedger (175 lines), KickCD (496) and LootHistory (416)
ship the doc; MultiMeters at 761 does not.

**Acceptance.**
- Each named repository carries the doc, and its `ARCHITECTURE.md` map row says Present.
- `documentation.md:237` states a threshold.
- MultiMeters at 761 lines is unarguable at any threshold; the marginal three stop being re-litigated
  each cycle.

**Non-goals.** Writing a `compat-layer.md` where no shim exists. Documenting LibKa0s's own shims in an
addon's doc.

---

## CX08 — a hard-coded texture path has a reason beside it

**Target.** `LibKa0s-Media` publishes roughly thirty marks (`lib.ICONS` at `Media.lua:92`, `lib.Icon` at
`:202`), and the collection carries hard-coded `Interface\` paths past them.

**The census, and the scope it is measured over, which is the whole of what went wrong here.** Over
tracked `*.lua`, excluding `libs/`, `tests/` and `PrettyChat/GlobalStrings/` — generated, unloaded,
`.pkgmeta`-ignored, and exempt by rule under `M1-STD-08` — the collection carries **75 lines holding 76
hard-coded `Interface\` paths**: BankLedger 17, LootHistory 19, ConsumableMaster 11, MultiMeters 8,
KickCD 7, PanelMaster 7, AbsorbTracker 3, WhatGroup 2, PrettyChat 1. **That is the ledger's original
figure, and it was right.** The triage "correction" to PrettyChat 93 counted the 92 hits inside the
generated `GlobalStrings/` tree this plan exempts by rule two sections later, and the "246
`Interface\Buttons\UI…` / 138 `Interface\Tooltips\UI…`" pair was measured over a scope that includes
`libs/` and `tests/` — nine vendored copies of the same Ace3 and LibKa0s payload, a tree every other
sweep in this plan explicitly excludes. Over the scope above those two figures are **4** and **3**. Two
other census counts in this cycle were wrong — `C22`'s eleven files against a measured 18, `C08`'s
"46 of 89" against 35 of 93 — and each came from a scope nobody wrote down. This one is the worst of the
three, because it was wrong **twice, in opposite directions**: filed right, corrected wrong, and the
correction was believed because it carried a bigger number. It is `M1-WA-02`'s reason for existing,
written against itself.

**What the 76 actually are.** Twenty-one are `Interface\Buttons\WHITE8x8`, the flat texture
`standalone-windows.md:20` itself mandates for the shared window edge. Twelve are
`Interface\AddOns\<Addon>\media\…` self-references to the addon's own shipped art. Neither is
something an icon catalog is meant to replace. What remains is Blizzard chrome the ~30-mark catalog
carries no equivalent for — the ReadyCheck marks, the chat size-grabber, the class circles, the
casting-bar spark — plus the two sites where the glyph **does** exist.

So the end state is a decision, per site, not a sweep. Where the catalog has the glyph, the site uses it:
`LootHistory/settings/Panel.lua:459-461`'s READY, NOTREADY and INFO_ICON, and
`MultiMeters/settings/ColumnBlocks.lua:60-61`'s `ENABLED_TEX`/`DISABLED_TEX`, which cite ConsumableMaster
parity and therefore move in both repositories together or in neither. Where it does not, the site carries
a reason beside it in the shape `LootHistory/modules/Browser.lua:1047-1051` already uses for its grip
texture, or a register row covers the class.

**Acceptance.**
- Over the scope stated above — tracked `*.lua`, excluding `libs/`, `tests/` and
  `PrettyChat/GlobalStrings/` — every remaining hard-coded `Interface\` path either has no catalog
  equivalent, or carries a one-line reason, or is covered by a register row naming the class. Vendored
  and generated trees are out of scope here for the same reason they are out of scope everywhere else in
  this plan, and the acceptance says so rather than leaving the reader to infer it.
- The command and its scope are written beside the number wherever the number appears.
- The two named pairs use `NS.Icon`, and the parity claim in MultiMeters' comment is still true.

**Non-goals.** Replacing Blizzard chrome the catalog does not carry. Editing anything under `libs/` or
`PrettyChat/GlobalStrings/`. Growing the catalog to cover Blizzard's button set.

---

## Explicitly out of scope for this entire plan

- **In-game verification as a claim.** Every in-client check in this bundle is an instruction to an
  operator. No statement in these documents rests on a client session having happened.
- **Any behaviour change not traced to a finding.** No refactors, renames or opportunistic cleanups.
- **Editing frozen bundles** — audits, reviews, automated-test bundles, revendor bundles.
- **Patching `libs/` or `tests/_kit/` in place** in any consumer, for any reason.
- **Rebinding `lib.MakeCloseButton`.** `CX06`'s answer is that the signature stays and the decline is
  ratified.
- **Splitting any file for `C22`** before `layout-§1` says what the cap binds. In particular MultiMeters'
  seven source files, which are the largest mechanical churn available here and collide with `C04`.
- **Backfilling `ANALYSIS.md`** into any of the 35 frozen bundles that lack one.
- **Renaming the `minimise` icon key.**
- **Annotating every TOC line** for `CX04`. Eight positions, not nine files.
- **Adding a second locale to any addon.** `C18` routes strings; it does not translate them.
- **Any release beyond the two LibKa0s tags** named in the surfaces table, plus whatever standard version
  the `M1-STD` rollup lands as. **Say the consequence out loud, because the plan's one urgency depends on
  it:** a re-vendor changes a repository, not a client. KickCD's eight empty dropdowns are repaired for a
  player by KickCD's next *release*, and this plan cuts none, so the shortest path in this bundle ends at
  a merged commit. Whether this cycle ships, and to which addons, is a decision for the owner and it is
  the fifth item in `00_OVERVIEW.md`'s decision list. Two things this plan does clear the way for it:
  `M4-25` and `M4-26` put KickCD and MultiMeters in a position to pass
  `automated-tests.md:143`'s release gate, which neither can today.
