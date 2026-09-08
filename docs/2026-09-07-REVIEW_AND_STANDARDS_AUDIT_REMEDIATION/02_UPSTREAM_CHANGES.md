# 02 — Upstream Changes (Milestone 1)

**Every change to LibKa0s, WowAddonStandards and the `wow-addon` plugin, in one place.**

> **Nothing in this bundle has been executed.** No tag has been cut, no payload copied, no section
> amended. Every item below is a proposal. The version numbers, tag names and adoption orders describe
> what *should* happen, not what has.

Item ids are scoped to this bundle: `M1-LK-nn` for LibKa0s, `M1-STD-nn` for WowAddonStandards,
`M1-WA-nn` for the plugin. They do not continue the 2026-08-05 bundle's numbering.

---

## The fact that shapes the whole milestone

**The collection is flat.** All nine consumers carry `Bundles LibKa0s … v1.25.0` in their root
`CLAUDE.md`, and all nine ship `Kit.VERSION = 14` at `tests/_kit/framework.lua:20`. Every vendored
`libs/LibKa0s/` and `tests/_kit/` payload is content-identical to the source once line endings are
ignored — 137 of 139 files byte-identical, the two exceptions being CRLF-only.

That flat baseline is what makes a multi-item release cheap, and it will not survive a partial rollout.
Every library-side cluster costs the same nine re-vendors, so shipping them one at a time costs four
waves where batching costs one. The plan below is therefore **two tags, not one and not seven**.

The second load-bearing fact is that a re-vendor wave does **not** have to be atomic.
`OptionsCompose.lua:29-35` gates on `lib.__composeMinor` and `lib.__composeShellMinor` against a fixed
`Options.lua` `MINOR`, so LibStub resolves the highest compose minor present in the session for every
consumer at once. Re-vendoring one addon with the fixed composer repairs the composed dropdowns in all
of them. That is why the critical fix can ship into a single repo first and be *seen working* before
eight more re-vendors are opened.

### The three upstream repositories

| Repo | Path | Role | Audited 2026-09-07? |
|---|---|---|---|
| LibKa0s | `/mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s` | The shared library **and** the shared test kit, both vendored into all nine addons. | Yes — review and audit both. |
| WowAddonStandards | `/mnt/d/Profile/Users/Tushar/Documents/GIT/WowAddonStandards` | The standard (v2.38.0, 2026-09-02) and the three playbooks. | **No.** No `reviews/`, no `audits/`, no bundle of any date. |
| wow-addon | `/mnt/d/Profile/Users/Tushar/Documents/GIT/wow-addon` | The plugin — the commands and the two agents that read the playbooks and act on addon repos. | **No.** |

Two of the three repositories that own the root cause of this milestone have never been audited. Both
are docs-only, which is presumably the reason, and `wow-addon/agents/review.md` (321 lines) plus
`WowAddonStandards/AUDIT.md` (515 lines) are what all twenty 2026-09-07 passes ran on. `M1-WA-06`
proposes closing that.

### Milestone 1 at a glance

| Group | Items | Clusters it unblocks | Findings closed here | Findings unblocked downstream |
|---|---|---|---|---|
| LibKa0s (`M1-LK-00` … `M1-LK-15`, the two tag cuts among them) | 16 | C01, C09, C10, C12, C17, C23, C24, C25, CX01, CX02, CX05 | 31 | ~40 |
| WowAddonStandards (`M1-STD-01` … `M1-STD-16`) | 16 | C02, C08, C10, C11, C14, C15, C16, C17, C22, C25, CX04, CX05, CX06, CX07 | 6 | ~75 |
| wow-addon plugin (`M1-WA-01` … `M1-WA-06`) | 6 | C08, C10, C19, C22 | 0 | ~30 |

**Group A closes 31 findings, and twenty of LibKa0s's own twenty-four are among them.** The four that are
not are `LIBKA0S-A-03` (the LOC cap, which waits on `M1-STD-08` to say whether it binds a library repo at
all), `LIBKA0S-R-02` (the `RESULTS.md` staleness, which waits on `M1-STD-07`), `LIBKA0S-R-15` (which
closes at `M1-STD-08` — see that item's own **Closes** line) and `LIBKA0S-A-14` (which closes at
`M1-STD-15`, likewise). The other eleven of the 31 are addon findings that close upstream: eight at the
test-kit runner, two at the line-ending repair and one at the geometry mock.

Group B closes six findings outright, in each case because the resolution **is** the rule change:
`PRETTYCHAT-A-09` and `WHATGROUP-A-15` via `M1-STD-03`, `LIBKA0S-R-15` via `M1-STD-08`, `KICKCD-A-10` and
`MULTIMETERS-A-12` via `M1-STD-11`, and `LIBKA0S-A-14` via `M1-STD-15`. Everything else in Groups B and C
is unblocked, not closed. **`BANKLEDGER-A-02` is not among them** — `M1-STD-04` makes its register row a
terminal compliant state, and the row itself is written at `M5-02`, which is where
`05_TRACEABILITY.md` maps it.

---

# Group A — LibKa0s

Path: `/mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s`. Two tags: **v1.26.0**, a fast payload fix,
and **v1.27.0**, kit plus convergence. Which item lands in which is stated per item and summarised at
the end of the group.

---

## M1-LK-00 · Repair seven LF working-tree files before anything else is tagged

**Files:** all seven listed below, not only the two in the payload. No code change, no minor bump.

**Verified problem.** `git ls-files --eol` reports exactly seven tracked files at `w/lf` under
`attr/text=auto eol=crlf` (the two `.sh` are correctly `eol=lf` and are not among them):
`LibKa0s/DebugLog.lua`, `LibKa0s/Pool.lua`, `tests/test_debuglog.lua`, `tests/test_pool.lua`,
`docs/api/Options/version-8.7.3-docs.md`, `docs/api/Options/version-9.7.3-docs.md`,
`docs/api/testkit/version-12-docs.md`. The first two are in the **shipped payload**.

`docs/releasing.md:133-134` gives the re-vendor its two checks:

```
diff -r --strip-trailing-cr LibKa0s <Addon>/libs/LibKa0s   # content — MUST be empty
diff -r LibKa0s <Addon>/libs/LibKa0s                       # bytes  — SHOULD be empty
```

The content diff passes. The byte diff does not, and will not, in **eight of the nine** repositories, on
every re-vendor, forever — `diff LibKa0s/LibKa0s/DebugLog.lua AbsorbTracker/libs/LibKa0s/DebugLog.lua`
reports 1,588 lines and `Pool.lua` 454, and `cmp` on `\r`-stripped content is identical. **PrettyChat is
the ninth and it passes today**, because its vendored copies of those two files are LF like the library's
working tree — which is `PRETTYCHAT-X-02`, and which means this repair *starts* PrettyChat's byte diff
failing until `M3-05` re-vendors it. That is the correct direction: one consumer briefly diverging from a
correct library beats nine permanently diverging from an incorrect one. Nobody has
chased it because `tests/_kit/vendor_sync.lua` strips CR against the git blob and therefore passes.
LibKa0s's own EOL gate cannot see them either: `tests/test_eol.lua:29` sets
`BUNDLES = "docs/automated-tests"` and scans nothing else.

**Change.** The index is already correct for all seven — only the working tree is wrong — so `rm` plus
`git checkout --` on **each of the seven** fixes it with no commit. `git add --renormalize .` does not:
it rewrites an index that was never wrong and leaves the working tree exactly as it found it. Do it
before either tag is cut, and **before the EOL gate is widened** — the widened gate reads working-tree
bytes, so repairing only the two payload files leaves five tracked files red with no item to fix them,
and the item that would sweep them sits behind the tag this milestone has to cut.

**Why it is first.** If it is not, the first thing nine re-vendors produce is roughly two thousand
lines of phantom diff on the check whose whole purpose is to say *the bytes match*, and the next reader
learns to skip that check.

**Unblocks:** C10 (the LibKa0s slice), and it is a hard prerequisite of `M1-LK-02`, `-05`, `-07`, `-08`.
**Adoption cost:** none. **Tag:** neither — it lands before v1.26.0.

---

## M1-LK-01 · The regression gate, in the same commit as `M1-LK-02`

**File:** `tests/test_options_compose.lua`. New cases only.

**Verified problem.** 764 green cases missed the Critical. The only `values` assertion in the composer
suite is at `tests/test_options_compose.lua:274`, against `O.VISIBILITY_VALUES`; nothing anywhere
invokes a media row's `values()`.

**Change.** Three cases asserting `type(rows[n].values()) == "table"` for `FontGroup`, `BorderGroup` and
`BarGroup`, plus **one more that pins the `__AttachCompose` contract**: a host-supplied `LSMValues` that
returns a table must be caught. That is the shape MultiMeters ships today and the shape `M1-LK-02`
silently demotes, so it is the one case that earns its place twice.

Write all four **red, before `M1-LK-02` touches `OptionsCompose.lua`**. This is the cheapest item in the
plan and the only reason the fix will not regress.

**Closes:** `LIBKA0S-A-01d`. **Adoption cost:** none — `tests/` is not vendored.
**Tag:** v1.26.0, same commit as `M1-LK-02`.

---

## M1-LK-02 · The composed media rows return a table-returner, not a closure

**File / symbol:** `LibKa0s/OptionsCompose.lua:231`, `:275`, `:304`. `COMPOSE_MINOR` (`:29`) 2 → 3.
Options version key `14.13.2.3` → `14.13.3.3`; new `docs/api/Options/version-14.13.3.3-docs.md`.

**Verified problem.** `O.LSMValues(mediaType)` (`LibKa0s/Options.lua:764`) already returns the deferred
closure the flow engine wants, and its own docstring at `:759-763` says the deferral is load-bearing —
"every LSM-backed row evaluates this inside a schema-row literal at FILE LOAD, long before the addons
that register media have run." The three group composers wrap it a second time:

```lua
values = function() return O.LSMValues("font") end,
```

`enumList` (`LibKa0s/OptionsWidgets.lua:78-79`) unwraps once, sees a function rather than a table, and
returns `{}`. The "no options" report at `OptionsWidgets.lua:1443` is gated at `:1442` on
`row.values == nil`, which is exactly the guard that keeps a legitimately-empty deferred list from
warning — so nothing prints. `git diff v1.25.0 HEAD -- LibKa0s/` is empty, so this is the shipped
behaviour in every consumer today.

**Change.** Three lines: `values = O.LSMValues("font")`, `("border")`, `("statusbar")`. No new surface,
no host signature moves, additive.

**The contract change nobody should discover in game.** `lib.__AttachCompose(O)`
(`OptionsCompose.lua:181`) lets a host supply its own `O.LSMValues`, and its own docstring says the
composers take `O` "because the media-backed rows call `O.LSMValues`, which is the instance's deferred
reader." Today the composer calls that member **inside a closure**, at dropdown-render time, so a host
supplying a *table-returner* works by accident. After this change the composer calls it **once, at
row-declaration time**, so a host's `LSMValues` must return a *function*.

**KickCD supplies one too, and this section missed it.** Corrected against shipped `e3274f6` by `M4-C2`.
`settings/Panel.lua`'s `function Helpers.LSMValues(mediaType)` returns the **hash**, and
`NS.Settings.Helpers` **is** the Options instance — decorated in place, never a fresh table — so that
function shadows `O.LSMValues` just as surely as an assignment would. The survey below looked for
`LSMValues =` and found MultiMeters; a shadow written as a decoration is invisible to that grep. The
consequence is identical and the requirement is identical: **KickCD MUST rewrite its shadow to return
the closure in the same commit as its re-vendor.**

The second-order error is worth keeping. Because KickCD shadowed with a table-returner, the composer's
extra closure deferred the read and **KickCD never had `LIBKA0S-A-01` at all** — measured at v1.25.0,
841 passed / 0 failed with all 16 media rows deferred. The adoption table said its rows "start working";
they were already working, and without the shadow rewrite the re-vendor is what would have **stopped**
them — 16 rows frozen at file load, 3 cases red, and in game no error at all. A host that works around a
defect is not a host that has it, and this section read the workaround as a symptom.

**MultiMeters supplies a table-returner.** `settings/Schema.lua:670` reads
`C.LSMValues = function(mediaType) return lsmValues(mediaType)() end` — it calls the closure and hands
back the table. Post-fix its composed rows receive a literal table, frozen at file load: no crash, no
warning, and precisely the failure `Options.lua:759-763` says the deferral exists to prevent.
**MultiMeters MUST revert `:670` to `C.LSMValues = lsmValues` in the same commit as its re-vendor.**
This is not optional and it is not a follow-up. AbsorbTracker and ConsumableMaster override `values`
after the composer returns and are unaffected.

**Closes:** `LIBKA0S-A-01` (the collection's only Critical), `ABSORBTRACKER-R-08`, and the whole of
`C01` and `CX01`.

**Adoption cost, per addon.**

| Addon | Cost |
|---|---|
| KickCD | Re-vendor **and** rewrite `Helpers.LSMValues` (`settings/Panel.lua`) to return the deferred closure, in the same commit. **Non-optional, exactly as for MultiMeters** — see the correction below. The eight composed sites (`settings/Castbar.lua:346`, `:481`, `:503`, `:514`, `:536`, `settings/Icons.lua:207`, `:258`, `settings/Label.lua:184`) emit 16 media rows across two units, and they **keep** working rather than start. |
| MultiMeters | Re-vendor **and** revert `settings/Schema.lua:670` in the same commit. Non-optional, per the contract change above. |
| AbsorbTracker | Re-vendor, then delete `LSM_KIND` and `fixMediaValues` (`settings/Appearance.lua:114-137`) and its three call sites at `:181`, `:237`, `:257`. The comment at `:121-129` says "delete this the re-vendor after the fix lands". |
| ConsumableMaster | Re-vendor, then delete `lsmValues` (`settings/MacroBar.lua:121-123`) and the three row overrides at `:269`, `:337`, `:454`. Close LibKa0s issue #15, which the comment at `:118` names. |
| BankLedger, LootHistory, PanelMaster, PrettyChat, WhatGroup | Re-vendor only. They consume `MasterControls` and `ColorPair`, no media composer; nothing moves. |

**Tag:** v1.26.0, on its own, because it is a shipped player-facing break.

---

## M1-LK-03 · Tab strip acquires from `LibKa0s-Pool-1.0` instead of creating per click

**File / symbol:** `LibKa0s/OptionsWidgets.lua` — `TabStrip` (`:1050-1072`), `makeTab` (`:942`),
`drawContentPanel` (`:643`), `releaseLedger` (`:874-880`). `WIDGETS_MINOR` (`:15`) 13 → 14.

**Verified problem.** `TabStrip` releases `__tabKids` and then rebuilds every button through `makeTab`
and the content panel through `drawContentPanel`, on **every click**, while `releaseLedger` only
`Hide()`s and `SetParent(nil)`s. WoW never collects frames, so an options panel leaks one button set
plus one panel per tab click for the life of the session.

The library ships `LibKa0s-Pool-1.0` at minor 3 and does not use it. Four consumers do —
`BankLedger/core/PoolSetup.lua`, `KickCD`, `LootHistory` and `MultiMeters`, plus `LedgerTable.lua`,
`IconGrid.lua`, `Row.lua` and `Window.lua` — so the library that published the pool is the one repo
that hand-rolls around it. `LIBKA0S-R-05` records a third, separate release contract in
`Widgets.lua:799-825`.

**Change.** Acquire buttons and the content panel from per-`ctx` pools; split `makeTab` into
`newTabButton` and `dressTab`; re-set `OnClick` on each dress. Internal to the library, no surface moves.

**Closes:** `LIBKA0S-R-01`, `LIBKA0S-R-05`, and `C23`. **Adoption cost:** re-vendor only, in all nine.
**Tag:** v1.26.0 if it is ready when the Critical is; v1.27.0 otherwise. It must not delay `M1-LK-02`.

---

## M1-LK-05 · `lib.__PatchLSM30Border()` — the one genuinely missing library surface

**File / symbol:** new function on `LibKa0s-Options-1.0`, guarded by `lib.__lsmBorderPatched`. Options
`MINOR` (`Options.lua:24`) 14 → 15.

**Verified problem.** Five addons ship a private `core/LSMPatch.lua`, each calling
`AceGUI:RegisterWidgetType("LSM30_Border", wrapper, currentVersion + 1)` against a **process-global**
registry: AbsorbTracker 50 lines, ConsumableMaster 65, PanelMaster 66, KickCD 68, MultiMeters 101 — five
distinct md5s. The last Ka0s addon to load owns that dropdown for every addon in the client, Ka0s or
not. A grep over `LibKa0s/*.lua` finds no `RegisterWidgetType` anywhere, so this is net-new surface, not
an unadopted one.

It belongs in the Options major on the evidence: `OptionsCompose.lua:274` is what declares
`dialogControl = "LSM30_Border"`, and `Options.lua:258` already takes `getLSM()` in the descriptor.

**Change.** `lib.__PatchLSM30Border()`, lib-level rather than per-instance, idempotent behind
`lib.__lsmBorderPatched` so five vendored copies register once. Additive; nothing existing moves.

**This is the one library change that cannot be proved headless.** The failure mode is "whichever addon
loaded last owns everyone's Border dropdown", and a headless suite cannot see the interaction at all.
Sequence it as: promote and re-vendor; **leave all five local copies in place**; smoke-test with
KickCD + PanelMaster + AbsorbTracker + ConsumableMaster + MultiMeters loaded together, opening each
addon's Border dropdown in turn; only then delete the five files, **in five separate commits**,
re-testing after the first. Deleting all five at once leaves no bisect point if the sentinel is wrong.

Note that the copies are not equally divergent, which changes the deletion order. KickCD and PanelMaster
are functionally identical; ConsumableMaster differs in a bootstrap header line and MultiMeters in a
`local _ = ...`; **AbsorbTracker is the real divergence** — it exposes a callable
`NS.ApplyLSMBorderPatch()` at `core/LSMPatch.lua:20`, invoked from `core/AbsorbTracker.lua:52`, rather
than a `PLAYER_LOGIN` frame. Delete AbsorbTracker's last.

**Closes:** `KICKCD-R-01`, `PANELMASTER-R-01`, and `C02`. **Blocked by:** `M1-STD-10` — until the rule
exists there is nothing for the finding to cite. **Adoption cost:** re-vendor in nine, one call site in
five, five deletions in five. **Tag:** v1.27.0.

---

## M1-LK-06 · The composed reset button reports instead of rendering dead

**File / symbol:** `LibKa0s/OptionsCompose.lua:393-402`, `LibKa0s/OptionsWidgets.lua:1313-1319`. New
`lib.STRINGS.DEAD_BUTTON`. Part of the Options major.

**Verified problem.** The composer builds `resetAll` and `resetPosition` **unconditionally**, whether or
not the spec supplies `onResetAll`/`onResetPosition`; `makeBtn`'s `OnClick` then returns early when
`spec.onClick` is nil. The result is a live-looking button that does nothing and says nothing. The
precedent for the cure is in the same file: `EMPTY_DROPDOWN` (`OptionsWidgets.lua:1443`) reports once at
build time and renders anyway.

**Change.** Add `lib.STRINGS.DEAD_BUTTON` and report once from `makeBtn` at build time.

**Stage it.** Because the composer builds `resetAll` unconditionally, **any host not passing
`onResetAll` newly prints** on the next re-vendor. Land the string and the report in v1.27.0, and audit
the nine specs for missing handlers in the same wave rather than shipping a chat line into nine
addons and calling it a diagnostic.

**Closes:** `LIBKA0S-R-08`, and with `M1-LK-12` and `M1-LK-13` the whole of `C24`. **Adoption cost:** re-vendor, plus
one spec audit per addon that composes a master group. **Tag:** v1.27.0.

---

## M1-LK-07 · The test-kit runner: skipped counts, release rows, and a lead-in that can be reached

**File:** `testkit/run-automated-tests.sh` — `:195`, `:369`, `:388`, `:414-432`. `Kit.VERSION`
(`testkit/framework.lua:20`) 14 → 15. New `docs/api/testkit/version-15-docs.md`.

**Verified problem — four defects, one file.**

1. The pass regex at `:195` is `'[0-9]+ passed, [0-9]+ failed(, [0-9]+ total)?'` while `framework.lua:566`
   prints `N passed, N failed, N skipped, N total`. The regex cannot span `, N skipped`, so the
   `awk '{print $5}'` total reads empty and `TESTS_TOTAL` silently falls back to `passed + failed`. A
   skipped case reads as a pass.
2. The manifest's `tests` object has no `skipped` key at all.
3. The trend row at `:388` renders `$ADDON_VERSION` only, so a release run shows the **pre-bump**
   version — `RESULTS.md:16` records `Version 1.24.0` for a bundle whose manifest carries
   `"release": "1.25.0"`.
4. The corrected four-checkpoint lead-in at `:414-432` sits in the branch reached only when
   `RESULTS.md` is **absent or header-mismatched**, so no existing repo can ever receive it. Ten
   `RESULTS.md` files still carry the old two-sentence text.

**Change.** Capture the skipped count; emit `passed/skipped/total` in the row and
`suites.tests.skipped` in the manifest, keeping the column name; render the version cell as
`version → release` when `manifest.release` is set; and rewrite the prose block above a matching header
while preserving the rows.

**Closes:** `LIBKA0S-A-06`, `-A-07`, `LIBKA0S-R-13`, `ABSORBTRACKER-A-05`, `BANKLEDGER-A-07`,
`CONSUMABLEMASTER-A-11`, `WHATGROUP-A-05`, `WHATGROUP-A-06`, and `C09`. **Adoption cost:** re-vendor
`tests/_kit/` in all nine; the payload is byte-identical today so no consumer has a local change to
reconcile. **Tag:** v1.27.0, paired with the payload — `docs/releasing.md:132` and `:199` copy both, and
each consumer's `tests/test_vendor_sync.lua` gates both against the one tag its provenance line names.

---

## M1-LK-08 · Frame geometry in the shared mock, in **two** kit revisions

**File:** `testkit/mock_base.lua:97`. `Kit.VERSION` 15 (additive half) then 16 (the flip).

**Verified problem.** `function f:GetHeight() return 0 end` for every frame, and the kit defines no
`SetAtlas` at all. `OptionsWidgets.lua:433-442` measures the tab-strip pitch from unselected atlas art,
so it always takes its `L.TAB_H` fallback, and any `options-ui-§13` geometry-invariance assertion passes
vacuously. Four repos filed the missing case and none of them can write one.

**Change, and why it is two revisions.** Roughly 308 test files across ten repositories lean on
`GetHeight` answering zero. Flipping it is a behavioural change to a shared mock, and every assertion
that passes today *because* geometry answers zero flips with it.

- **Kit 15 (additive).** Add `SetAtlas(name, useAtlasSize)` writing a height from a kit-published atlas
  table, plus an opt-in `f:__setGeom(w, h)`. Nine repos take it and nothing moves.
- **Kit 16 (the flip).** Change `GetHeight`'s default, once each consumer has adopted the opt-in where
  it needs geometry.

Shipping both at once is the version of this that costs a week of red suites in nine repositories
simultaneously.

**Closes:** `ABSORBTRACKER-A-10`, `MULTIMETERS-A-08`, `PANELMASTER-A-07`, `PRETTYCHAT-A-10`, and `C12`.
**Adoption cost:** kit 15 none; kit 16, one geometry case per repo that wants one, plus whatever the
default flip reddens. **Tag:** kit 15 in v1.27.0; kit 16 in a later tag, after adoption.

---

## M1-LK-09 · `Kit.assertSurfaceParity` and a machine-readable member manifest

**File:** `testkit/framework.lua` — new `Kit.assertSurfaceParity(stub, majorName)`. New
`docs/api/<Major>/members.json` (or an equivalent the versioning suite already derives). Kit 15.

**Verified problem.** Nine addons hand-write a `settings/OptionsSetup.lua` degradation arm mirroring
the `LibKa0s-Options-1.0` surface: MultiMeters 384 lines, AbsorbTracker 369, KickCD 351, PrettyChat 265,
WhatGroup 258, BankLedger 230, PanelMaster 217, LootHistory 199, ConsumableMaster 185. Only three carry
a `tests/test_surface_parity.lua`. That is how AbsorbTracker's stub omits `SetRenderer` entirely with
every suite green (`CX03`).

**The obvious fix is wrong and should not be attempted.** A published no-op surface would have to live
in the payload that is **by definition absent** on the path the stub exists for — `AbsorbTracker/settings/OptionsSetup.lua:44`
opens with `local lib = LibStub and LibStub("LibKa0s-Options-1.0", true)` and the stub is the arm below
it. A library cannot ship the thing that stands in for the library's absence.

**Change.** Move the work kit-side: a `Kit.assertSurfaceParity(stub, majorName)` factory plus a
machine-readable member list under `docs/api/`, so the nine stubs are checked against the live surface
rather than hand-maintained against a reading of it.

**Closes:** the addressable half of `CX02`. **Adoption cost:** one three-line case per repo, six of
which have nothing today. **Tag:** v1.27.0, kit 15.

---

## M1-LK-10 · The EOL gate reads the tracked set, and moves into the kit

**File:** `tests/test_eol.lua:29` → `testkit/` (new kit member). Kit 15.

**Verified problem.** `line-endings-§7` (`line-endings.md:362-370`) MUSTs the four properties be checked
**mechanically** by an audit and supplies the command. Ten of ten repositories fail it — including two
files inside LibKa0s's own shipped payload (`M1-LK-00`). The gate that would catch it already exists,
wired at `tests/run.lua:117`, and is scoped to `docs/automated-tests` by
`tests/test_eol.lua:29`'s `BUNDLES` constant.

**Change.** Widen `trackedFiles()` to the whole `git ls-files` set, keep the NUL guard, and move the
suite into the vendored `tests/_kit/` so all nine inherit it.

**Why this is an addition and not a sweep.** `C10` has been a recurring ten-repo working-tree sweep
across cycles. With the gate widened and vendored it becomes a red test, once, and stops coming back.
Per addon, `git add --renormalize .` produces **no index change** — the index is already LF-normalised
everywhere — so the per-repo work is a working-tree fix, not a churn commit, and conflicts with nothing.

**Closes:** `LIBKA0S-R-04`; converts the rest of `C10` from a sweep into a gate. **Adoption cost:**
re-vendor, then one working-tree renormalise per repo. **Tag:** v1.27.0, kit 15.

---

## M1-LK-11 · The prose gate stops reading as coverage it does not provide

**File:** `tests/test_prose.lua:113`; `LibKa0s/Media.lua:94`; `LibKa0s/Perf.lua:723`, `:864`, `:948`,
`:1029`, `:1063`.

**Verified problem.** `localization.md` names its own enforcement as review plus
`/wow-addon:standards-audit` and gives a Use/Never prose table rather than a list. LibKa0s built a
mechanical gate anyway, and it is
`BRITISH = { "colour", "grey", "behaviour", "synthesise", "normalis", "recognis" }` — six substrings,
two of which are not in the section's table at all. It stays green while `minimise` ships as a **public
`lib.ICONS` key** (`Media.lua:94`) and `CANCELLED` reaches chat text a player reads (five sites in
`Perf.lua`). A gate that reads as coverage and provides none is `testing-§12`'s exact failure mode,
sitting inside the gate for `localization-§5`.

**Change.** Widen the list — at minimum `minimis`, `centre`, `cancelled`, `labelled`, `travelled`,
`organis`, `optimis`, `initialis`, `customis` — and sweep the authored prose and the five `Perf.lua`
chat strings.

**Do not rename the icon key.** `lib.Icon` (`Media.lua:202`) builds the path **from** the key —
`base .. ICON_DIR .. "\\" .. name` — and the file on disk is `minimise.tga`, vendored into all nine
`libs/LibKa0s/media/icons/` trees. Adding `"minimize"` to `lib.ICONS` alone yields a path to a file that
does not exist, which is the silent failure `Media.lua:190-196` records: a texture that fails to load
draws nothing and raises nothing. If the key is ever to change it needs a second `.tga` or an alias map;
until then, the key stays and the register carries a row. Live consumers of it are
`MultiMeters/modules/HeaderControls.lua:127` and `core/Diagnostics.lua:333`.

**Closes:** `LIBKA0S-A-08`, `LIBKA0S-A-08d`, and the library half of `C17`. **Depends on:** `M1-STD-12`,
so the widened list is the section's list rather than a second private one. **Adoption cost:** none
beyond the re-vendor. **Tag:** v1.27.0.

---

## M1-LK-12 · The library's own lint config, as the pilot for ten repos

**File:** `.luacheckrc:4`.

`.luacheckrc:4` excludes `{ "tests/", "docs/" }`, so lint's clean result covers 18 of 49 tracked Lua
files. Only `tests/_kit/` is genuinely redundant with `testkit/`, which lints as source. Narrow the
exclusion to `tests/_kit/` and add a `files["tests/"]` stanza declaring `LK_TEST`, rather than widening
top-level `read_globals` — a global declared at the top level is a global the library's own source may
then use unchallenged.

**Why it is its own item.** This is the pilot for `CX05`, `M1-STD-01` and `M4-11`. The config shape is
proved in one repository before it is written into the standard's template and taken by nine more, and
that ordering is the whole reason the item exists separately from the four bullets in `M1-LK-13`.
`M1-STD-01` depends on it.

**Closes:** `LIBKA0S-R-09`. **Adoption cost:** none — `.luacheckrc` is not vendored, and the nine take
this shape at `M4-11` against the template rather than from here. **Tag:** v1.27.0.

---

## M1-LK-13 · Four library-local repairs: the printer, the bracket slots, the shim and one comment

**Files:** `LibKa0s/OptionsWidgets.lua:696` against `LibKa0s/Options.lua:289-291`;
`LibKa0s/Perf.lua:478`; `LibKa0s/Perf.lua:615-618`; `tests/run.lua:110-118`.

Four small library-local items with no adoption cost beyond the re-vendor, grouped because none of them
is worth its own release.

- **`OptionsWidgets.lua:696`** is `local print = d.print or function() end` — no type guard, no
  `DEFAULT_CHAT_FRAME` fallback, where `Options.lua:289-291` has both. It discards `NO_GROUPS`,
  `EMPTY_DROPDOWN` and `BUTTON_FAILED`, which is part of why C01 shipped silently. Store the shell's
  constructed sink as `O.__print` and have `__AttachWidgets` read it. Closes `LIBKA0S-R-06`.
- **`Perf.lua:478`** allocates `{ key = key, t0 = debugprofilestop() }` per bracket in the capture arm,
  and only the dormant path is measured (`tests/test_perf_isolation.lua:66`). Reuse slots via a
  high-water free list, state the active-arm cost in the docstring, add the active-arm case. Closes
  `LIBKA0S-R-07`.
- **`Perf.lua:615-618`** calls `GetSpecialization`/`GetSpecializationInfo` with no namespaced rung,
  while `Env.lua:60-66` models the `C_AddOns` shim for exactly this shape. Take
  `C_SpecializationInfo.GetSpecialization` first. Closes `LIBKA0S-A-10`.
- **`tests/run.lua:110-118`** hand-types a 22-name suite list beside an XML load list at `:24` that is
  derived and commented. The hand-typed list is held honest by `Kit.assertSuiteInventory`
  (`testkit/framework.lua:277`) and says so nowhere. One comment. Closes `LIBKA0S-R-11`.

**Closes:** `LIBKA0S-R-06`, `LIBKA0S-R-07`, `LIBKA0S-A-10`, `LIBKA0S-R-11` — and with `M1-LK-06` and
`M1-LK-12`, all of `C24`. **Adoption cost:** re-vendor only. **Tag:** v1.27.0.

---

## M1-LK-14 · Release preconditions and the standards pointer

**Files:** `CLAUDE.md:3`, `README.md:3`; `docs/releasing.md`.

**Verified problem.** Both standards pointers read v2.28.0; `WowAddonStandards/standards/STANDARDS.md:1`
reads **v2.38.0 (2026-09-02)**, and the `options-ui-§15`–`§18` sections `OptionsCompose.lua` cites
arrived at v2.38.0. Separately, tag `v1.24.0` exists with no release bundle naming it — the bundles
jump 1.23.0 to 1.25.0 — and the `20260903-161751` bundle records `dirty: true` at sha `895cdf4`, so a
release run is stamped reproducible from a tree it cannot be reproduced from.

**Change.** Move both pointers to v2.38.0 and add a pointer check to `docs/releasing.md`'s order.
Make the four-suite bundle a hard precondition of the tag, and have the runner refuse to stamp a dirty
run as a release.

**The precondition that already binds and should be stated as such.** `docs/releasing.md` step 5 is
**enforced, not remembered**: `tests/test_versioning.lua:159-181` derives
`docs/api/<Major>/version-<key>-docs.md` from the live `lib.MODULES` table and stays red until the
document exists. So every minor bump in this group — Options 14 → 15, Compose 2 → 3, Widgets 13 → 14,
Kit 14 → 15 — makes step 7's green gate unreachable until its API document is written. That is a
feature; write the documents with the code, not after the tag.

**Closes:** `LIBKA0S-R-10`, `LIBKA0S-R-12`, `LIBKA0S-A-04`, `LIBKA0S-A-05`, and `C25`'s library half.
**Adoption cost:** none. **Tag:** v1.27.0.

---

## Group A tags — `M1-LK-04` and `M1-LK-15`

The two tag cuts are work items in their own right, numbered in sequence with the items they carry:
**`M1-LK-04` cuts v1.26.0** and **`M1-LK-15` cuts v1.27.0**. Both run `docs/releasing.md` steps 1–7.

**v1.26.0 — payload, fast (`M1-LK-04`).** `M1-LK-00` (before the tag), `M1-LK-01`, `M1-LK-02`, and
`M1-LK-03` if it is ready. Cut it on its own: `M1-LK-02` is a shipped player-facing break and should not
wait on `M1-LK-05`'s design or the kit work.

Minors moving: `COMPOSE_MINOR` 2 → 3. Options version key `14.13.2.3` → `14.13.3.3` (or
`14.14.3.3` with `M1-LK-03`).

**v1.27.0 — kit plus convergence (`M1-LK-15`).** `M1-LK-05` through `M1-LK-14`.

Minors moving: Options `MINOR` 14 → 15, `WIDGETS_MINOR` 13 → 14 if `M1-LK-03` slipped,
`Kit.VERSION` 14 → 15.

Kit and payload move in **one** tag because `docs/releasing.md:132` and `:199` copy both, and each
consumer's `tests/test_vendor_sync.lua` asserts both against the one tag its `CLAUDE.md` provenance line
names. Two tags means two re-vendors per addon, which is the floor here: the kit work cannot wait on
`M1-LK-05`'s design, and `M1-LK-02` cannot wait on the kit.

---

# Group B — WowAddonStandards

Path: `/mnt/d/Profile/Users/Tushar/Documents/GIT/WowAddonStandards`, at v2.38.0 (2026-09-02).

Two items here are not amendments in the usual sense: they **reverse a disposition**. `CX04` and `CX05`
as triaged would cost ten repositories a body of work the standard's own text does not require. Both
lead the group, because a plan that ships them as filed is worse than a plan that ships nothing.

---

## M1-STD-01 · `lint` — narrow the `tests/` exclusion, do not ask ten repos to violate the template

**Section:** `lint.md:11` (the template) and `lint.md:32` (the normative sentence).
**Reverses:** `CX05`'s `per-addon` disposition.

**Verified problem.** `CX05` is right about the fact and wrong about the direction. Counted over
`git ls-files '*.lua'` excluding `libs/` and `tests/_kit/`, the collection holds **329 source files
against 308 test files**, and every `.luacheckrc` excludes the whole `tests/` tree — so every
`RESULTS.md` clean-lint claim covers a little over half the Lua.

But the exclusion is not addon drift. `lint.md:11` ships it *as the template*:

```lua
exclude_files = { "libs/", "docs/audits/", "docs/reviews/", "_dev/", "tests/" }
```

and `lint.md:32` states it normatively: "`tests/` is excluded from lint (the harness is exercised by
running it, not by linting it)." All ten repositories comply exactly. The triaged disposition asks ten
repos, at effort M each, to do the opposite of what the section tells them.

**Change.** Amend `lint.md`: narrow the exclusion to `tests/_kit/` and add a `files["tests/"]` stanza
declaring the kit globals, so a test file is linted against the right global set rather than the source
one. `LIBKA0S-R-09` already proposes exactly this against `.luacheckrc:4`.

**Stage it.** Turning 308 test files on at once produces a wall that gets silenced with a blanket
ignore, which is worse than the exclusion. `M1-LK-12` proves the config shape in LibKa0s first; the
amendment then propagates a shape that is known to work.

**Unblocks:** `CX05`, `LIBKA0S-R-09`, `WHATGROUP-A-14`. **Adoption cost:** one `.luacheckrc` edit per
repo plus whatever the newly-linted tests report — unknown until LibKa0s runs it, which is the point of
staging.

---

## M1-STD-02 · `toc-file-§5` — the MUST already binds narrowly; the SHOULD is what is unmet

**Section:** `toc-file.md:144` (the load-bearing MUST) and `:147` (the conventional SHOULD).
**Reverses:** `CX04`'s scope.

**Verified problem.** `CX04` counts annotations against all 23–81 lines of nine TOCs and concludes a
MUST that nobody satisfies. The rule does not say that. `toc-file.md:144` reads:

> A line whose position is **load-bearing MUST** carry a comment saying so, at the line, naming
> **what resolves at load** — not merely that the order matters.

It binds load-bearing lines only. Measured against that denominator the per-repo audits applied it
correctly and small: `KICKCD-A-02` names two positions, `PRETTYCHAT-A-01` names two after correctly
dropping a third, `WHATGROUP-A-02` names four. `AbsorbTracker.toc:39-40` is a compliant instance. That
is roughly eight one-line additions, not a rule to rewrite and not nine TOCs to annotate.

What **is** near-universally unmet is `toc-file.md:147`'s *conventional* SHOULD — a note once per group
saying which lines are safe to move. That is a SHOULD, and it does not make the MUST wrong.

**Change.** No normative change to `:144`. Add a worked example distinguishing the two, so the next
audit measures the MUST against load-bearing lines and files the SHOULD separately, and correct
`CX04`'s disposition to the eight addon-local one-liners it actually is.

**Unblocks:** `CX04`, `KICKCD-A-02`, `PRETTYCHAT-A-01`, `WHATGROUP-A-02`. **Adoption cost:** eight
one-line TOC comments across three repos, plus an optional group note per repo.

---

## M1-STD-03 · `documentation-§3` — name the fourth table, because nine of nine wrote it

**Section:** `documentation.md:279` (the "exactly one of its three tables" MUST) and the template's
three table headings at `:290`, `:297`, `:304`.

**Verified problem.** `documentation.md:279` MUSTs that every `.md` under `docs/` appear "in **exactly
one** of its three tables". Seven documents belong to no tier: `testing.md`, `smoke-tests.md` and the
five verification-and-record docs — which `§3` itself places **outside** the tier model. The register is
therefore unsatisfiable as written, and all nine addons independently wrote the same workaround. Every
one carries a `### Verification and record` table: AbsorbTracker `docs/ARCHITECTURE.md:332`, BankLedger
`:199`, ConsumableMaster `:287`, KickCD `:204`, LootHistory `:360`, MultiMeters `:660`, PanelMaster
`:148`, PrettyChat `:190`, WhatGroup `:320`.

`C16` records two of the nine, because only two audits thought to file a rule they were all quietly
working around.

**Change.** Amend `§3` to name a fourth table, and settle whether `ARCHITECTURE.md` registers itself.

**Ripple, and it reaches the plugin.** Three documents outside the section restate the three-table
shape and move with it: `NEW_ADDON.md:204`, `wow-addon/commands/new-addon.md:87` and
`wow-addon/commands/sync-docs.md:12` — the last of which enumerates the frozen directories and would
otherwise keep writing a three-table register into every `sync-docs` run.

**Closes:** `PRETTYCHAT-A-09`, `WHATGROUP-A-15`, and `C16`. **Unblocks:** the `C15` rows that are
register-shape questions rather than heading drift. **Adoption cost:** nine repos delete a
self-justifying note; none moves a table.

---

## M1-STD-04 · `standalone-windows` — the close-button MUST and MAY contradict each other

**Section:** `standalone-windows.md:30` against `:34`.

**Verified problem.** `:30` reads "every close control it builds, on any window, **MUST** be built
through that wrapper", strengthened from SHOULD at v2.32.0 and argued at length. `:34` reads "a host
**MAY** draw a different one on **its own** windows where the design calls for it". BankLedger
(`core/CoreSetup.lua:117-129`) and LootHistory (`core/CoreSetup.lua:19-26`) each recorded a deliberate
decline citing exactly that MAY. They are compliant under `:34` and defective on sight under `:30`, and
no audit can grade them without picking one.

**Change.** Reconcile the two. Either `:34`'s MAY is narrowed to the library-drawn windows `:34` itself
carves out, or `:30`'s MUST gains the MAY as an explicit exception with a register row as its price.

**Two corrections that belong in the same edit.** First, `CX06`'s "BankLedger and LootHistory declined"
is one release stale: LootHistory's own comment at `core/CoreSetup.lua:19-26` records the decline as
**expired** at LibKa0s v1.10, and `:167` is now a compliant wrapper. **BankLedger is the only live
decline in the collection.** Second, `CX06`'s proposed cure — binding `addonName` inside the library —
is contradicted by the library's own recorded reasoning at `LibKa0s/Media.lua:14-20`: `...` carries the
addon name only for a file the TOC loads directly, so there is nothing to infer from. See
"Recommended not to do" below.

**Closes:** nothing directly. **Unblocks:** `CX06`, and `BANKLEDGER-A-02`, whose register row is written
at `M5-02` and is only a terminal compliant state once the MUST and the MAY stop contradicting each
other. **Adoption cost:** one register row in BankLedger.

---

## M1-STD-05 · `library-stack-§1` and `§3` collide, and PrettyChat carries a row for the collision

**Section:** `library-stack.md:9-14` (the mandatory-libs table) against `library-stack.md:39`.

**Verified problem.** `:9-14` lists AceEvent-3.0 and AceTimer-3.0 in "Mandatory libs (every Ace3
addon)", vendored. `:39` MUSTs "vendor only libs the addon actually `LibStub(\"X\")` — vendor what you
use, nothing more. Prune dead weight." PrettyChat uses neither, so it must both vendor and not vendor
them, and it registers the contradiction at `docs/ARCHITECTURE.md:230`.

An addon holding a deviation row for a defect that lives upstream is precisely the graveyard the
register exists to prevent, manufactured by the standard.

**Change.** Mark AceEvent/AceTimer — and arguably AceGUI, for an addon with no settings panel — as
mandatory-**when-used**, or state that `§3`'s prune rule governs the table.

**Closes:** the PrettyChat row in `C14`. **Adoption cost:** PrettyChat deletes one register row.

---

## M1-STD-06 · `line-endings-§4` and `§5` collide on an extension-less binary

**Section:** `line-endings.md:117-131` (`§4`) against `line-endings.md:133-135` (`§5`).

**Verified problem.** `§4` MUSTs every binary type be marked and forbids trimming the list. `§5` MUSTs
`.gitattributes` be one of two canonical bodies, byte-for-byte. `PanelMaster/.gitattributes:70` carries
`tools/artwork/bin/realesrgan-ncnn-vulkan binary` — an extension-less path an extension-keyed union
cannot express — giving 86 lines against KickCD's canonical 81. `PanelMaster/docs/ARCHITECTURE.md:197`
records it as "Two MUSTs collide and only one can hold", and `§4`'s own text cites this repo's `.param`
as its live example, so the standard already knows the repository.

**Change.** `§5` sanctions a clearly delimited appendix block below the canonical body for
repo-specific extension-less binaries, so an auditor still diffs rather than reads.

**Closes:** the PanelMaster half of `C10`. **Adoption cost:** PanelMaster re-orders one file.

---

## M1-STD-07 · `automated-tests-§4` mandates prose `documentation-§3` forbids anyone to write

**Section:** `automated-tests.md:223-224` and `:236` against `documentation.md:180`.

**Verified problem.** This contradiction, and not addon laziness, is why `C08` is stale in all ten
repositories. `documentation.md:180` calls `docs/automated-tests/RESULTS.md` "**generated**, never
hand-edited". `automated-tests.md:223-224` MUSTs a per-entry disposition — "*accepted and why*",
"*peel next*", "*already tracked as `<deviation-id>`*" — and `:236` MUSTs "a short standing section for
each of the **other three** suites". No generator produces narrative of that kind, and
`testkit/run-automated-tests.sh` writes none of it. `automated-tests-§3` has no gate that reads the
file either.

**The cluster's numbers are also wrong.** 93 bundles hold no `ANALYSIS.md` in 35 of them, not "46 of
89" — and `automated-tests.md:245` makes the write-up a MUST only for **release** runs, so most of the
35 are the SHOULD.

**Change.** Settle `§4` against `documentation-§3` first: either the dispositions are generated (which
means they are data the runner can emit) or `RESULTS.md` is a partly-authored document and
`documentation.md:180` is wrong about it. Then re-count.

**Unblocks:** `C08`, which is the collection's only XL. A large part of that XL is probably not work.
**Adoption cost:** unknown until the contradiction is settled, which is the argument for settling it
before scheduling anything.

---

## M1-STD-08 · `layout-§1`'s cap, and `library-stack-§7`'s missing third list

**Sections:** `layout.md:55` (the cap) and `library-stack.md:175-207` (the two applicability lists).
One decision, two files.

**Verified problem — the cap is undefined in three directions.** `layout.md:55` MUSTs a cap on "any
single `.lua` file" with no carve-out for tests, generated data or a library repo, and the collection
answered the silence three different ways: ConsumableMaster filed `CONSUMABLEMASTER-A-06` for a test
file, MultiMeters filed none of its six, LibKa0s filed `LIBKA0S-A-03` and held it at low, and PrettyChat
registered a deviation at `docs/ARCHITECTURE.md:221` asking for "a layout revision that sanctions a
generated-data folder".

The census the decision has to cover is **18 files**, not `C22`'s eleven. Seven MultiMeters source files
(`settings/Schema.lua` 3069, `modules/Tooltip.lua` 2652, `modules/Window.lua` 2644,
`modules/Aggregator.lua` 2058, `modules/Export.lua` 1743, `core/Diagnostics.lua` 1726, `modules/Row.lua`
1702) plus seven MultiMeters test files (`tests/test_window.lua` 2737, `test_tooltip.lua` 2708,
`wow_mock.lua` 2265, `test_row.lua` 1606, `test_aggregator.lua` 1605, `test_schema.lua` 1573,
`test_export.lua` 1509), `ConsumableMaster/tests/test_macrobar.lua` 1894,
`PrettyChat/GlobalStrings/GlobalStrings.lua` 23,842, and LibKa0s's `LibKa0s/OptionsWidgets.lua` 1838 and
`tests/test_options_widgets.lua` 2287. **KickCD and PanelMaster have none** — their largest are 1320 and
1356, so the findings filed against them are band and complexity items, not cap breaches.

**Verified problem — the applicability lists are not exhaustive.** `library-stack.md:175-207` gives
"Applies, unchanged" (8 rows) and "Does not apply" (`documentation-§1`/`§2`/`§3`, `toc-file`,
`options-ui`, `slash-commands`, `preview-mode`, `savedvariables`, `packaging`). Absent from both:
`layout`, `architecture`, `performance`, `compat`, `anti-patterns`, `public-api`, `debug-logging`,
`events-frames-taint`, `standalone-windows`, `naming-cheatsheet`, `audit-review-history`,
`documentation-§4`. So LibKa0s's own two cap breaches are **unclassified**, which is why
`LIBKA0S-A-03` correctly sits at low.

**Change.** Answer three questions in `layout-§1` — does the cap bind `tests/`, does it bind generated
non-shipping data, does it bind a library repo — and give `library-stack-§7` the applicability list it is
missing, naming the remaining sections, or state a default with the two existing lists as exceptions.
Note while there that `§7`'s own block at `:175-179` says "the three lists below" and the third of them
(*Substitutes*, `:211-228`) answers a different question, so the count in that sentence moves too.

**Closes:** `LIBKA0S-R-15`. **Unblocks:** `C22`, `LIBKA0S-A-03`, `CONSUMABLEMASTER-A-06`,
`MULTIMETERS-R-08`. **Adoption cost:** potentially zero. Depending on the answer, most of `C22` is not
a breach at all — see "Recommended not to do".

---

## M1-STD-09 · `packaging`'s own template fails `packaging`'s own strong-form MUST

**Section:** `packaging.md:9-24` (the minimum template) against `packaging.md:28`.

**Verified problem.** `:28` MUSTs that "Every root dotfile and dot-directory present in the repo MUST
either appear in `.pkgmeta`'s `ignore:` list or be justified in a comment beside it." The template at
`:9-24` lists `.luacheckrc`, `.gitignore`, `.gitattributes`, `.claude`, `.superpowers`, `docs`, `tests`,
`_dev` and `*.bak` — and not `.pkgmeta` itself, which is a root dotfile present in every repo. Only
ConsumableMaster and MultiMeters ignore it; the other seven followed the template.

**Change.** One template line, which closes that half of `C11` in seven repositories at once.

The rest of `C11` is genuine non-compliance against a template that already names the offenders, and it
is worth separating from the template defect because the reach differs sharply: `AbsorbTracker/.pkgmeta`
omits `.superpowers`, and `du -sh` on it reports **2.8M of tracked review diffs** that every player
downloads. `WhatGroup/.pkgmeta:6-19` ignores `.claude` but not `media/screenshots` (880K), root
`CLAUDE.md` or `DEPENDENCIES.md`. `LootHistory` carries an unignored, unjustified `.pytest_cache`,
which is exactly what `:28`'s strong form exists for. Three other filings — `BANKLEDGER-A-03`,
`MULTIMETERS-A-04`, `WHATGROUP-A-13` — were rejected in triage because the directories they name are
gitignored, empty or absent.

**Closes:** the template half of `C11`. **Adoption cost:** one line per repo, plus the four real
omissions.

---

## M1-STD-10 · A widget-registry mutation is a library concern, and anti-pattern #76

**Sections:** `library-stack` (new rule), `anti-patterns` (new entry — the list ends at **#75**).

**Verified problem.** Five repositories ship a private `core/LSMPatch.lua` re-registering `LSM30_Border`
at a higher version into AceGUI's **process-global** widget registry (AbsorbTracker 50 lines,
ConsumableMaster 65, PanelMaster 66, KickCD 68, MultiMeters 101, five distinct md5s). `anti-patterns` #8
explicitly **sanctions** `RegisterWidgetType` extension over forking a widget, and nothing anywhere in
the standard addresses the blast radius: the last Ka0s addon to load rewrites that dropdown for every
addon in the client, Ka0s or not.

**Change.** A rule — a widget-type re-registration is a `LibKa0s` concern, never a per-addon one — plus
anti-pattern **#76** naming the process-global tell, so an auditor can recognise the next one without
having to reason from scratch about AceGUI's registry.

**Blocks:** `M1-LK-05`. Until the rule lands, `KICKCD-R-01` and `PANELMASTER-R-01` have nothing to cite,
which is exactly why one bundle graded it High and the other Medium. **Adoption cost:** none directly;
`M1-LK-05` carries it.

---

## M1-STD-11 · `options-ui-§1` — rule on composers without the Options major, and on the broadcast meta row

**Sections:** `options-ui-§1`; `options-ui-§16`.

**Verified problem, two rulings the addons cannot make for themselves.**

`KICKCD-A-10` (`docs/ARCHITECTURE.md:241`, `:244-261`) carries a register row that says outright it is a
recorded decision **under review**, not a ratified deviation: a library-less load registers 112 of
KickCD's 228 rows, because the composed half of the schema is built by a library that is absent. Either
composers may ship without the Options major, or `options-ui-§1` states which of its MUSTs wins. No
local fix exists.

`MULTIMETERS-A-12` (`settings/Schema.lua:1553-1566`): `options-ui-§16`'s grep flags
`window.barTexture` and `window.font` as hand-written media groups. They are not — they are single
All-surfaces rows with `LSM30_` dialog controls and `broadcastBarTexture`/`broadcastFont` `onChange`
handlers, an addon-wide broadcast meta row the section has no shape for.

**Change.** Rule on the first. For the second, narrow `§16`'s clause to hits that reproduce a mandated
block, or have `LibKa0s-OptionsCompose` expose a broadcast-meta composer.

**Closes:** `KICKCD-A-10`, `MULTIMETERS-A-12`. **Adoption cost:** depends on the ruling; possibly zero.

---

## M1-STD-12 · `localization-§5` publishes the substring list its own table implies

**Section:** `localization.md:118+`.

**Verified problem.** `§5` names its enforcement as review plus `/wow-addon:standards-audit` and gives a
Use/Never prose table rather than a machine-readable list. The one repo that automated it anyway
invented its own six-substring list, two entries of which are not in `§5`'s table, and it misses every
live hit in the collection — see `M1-LK-11`.

**Change.** Publish the canonical substring list `§5`'s table implies, and require a mechanical gate to
use it **whole** rather than a subset.

**Unblocks:** `C17`, `LIBKA0S-A-08d`, `CONSUMABLEMASTER-A-02`, `KICKCD-A-03`, `WHATGROUP-A-09`.
**Adoption cost:** the sweeps those findings already name; the amendment stops the next gate from being
a private guess.

---

## M1-STD-13 · `line-endings-§7` gets the seam it has never had

**Section:** `line-endings.md:362-370`.

**Verified problem.** `§7` MUSTs the four properties be checked mechanically by an audit and supplies
the command. It is the collection's only **100%-failed MUST** — ten of ten repositories, including two
files inside LibKa0s's own shipped payload. The rule is right and the fix is one
`git add --renormalize .` per repo, which is why it keeps coming back.

**Change.** Cite the widened, vendored gate `M1-LK-10` builds. This is an addition rather than an
amendment: with a red test in every repo, `C10` stops being a recurring ten-repo sweep.

**Depends on:** `M1-LK-10`. **Unblocks:** `C10`. **Adoption cost:** one working-tree renormalise per
repo, which produces no index change.

---

## M1-STD-14 · `documentation-§3`'s `compat-layer.md` trigger gets a number

**Section:** `documentation.md:237`.

**Verified problem.** `:237` reads "`core/Compat.lua` carries **addon-specific** shims beyond what
`LibKa0s` supplies" — pure judgment, where `docs/slash-dispatch.md` got "**eight or more** commands"
(`:235`) and `docs/message-bus.md` got "**more than ten**" (`:238`). Four repos read it four ways:
MultiMeters ships 761 lines of `core/Compat.lua` and no doc, ConsumableMaster 83 and no doc, WhatGroup
130 and no doc; BankLedger (175), KickCD (496) and LootHistory (416) all ship one.

**Change.** Give the trigger a number.

**Unblocks:** `CX07`. MultiMeters at 761 lines and 31 shims is not arguable and stays addon work either
way; the marginal three stop being re-litigated every cycle. **Adoption cost:** none; it removes work
rather than adding it.

---

## M1-STD-15 · Two register rules, and the module inventory that is one file behind

**Sections:** `audit-review-history.md:32-39`; `library-stack.md:70` and `:82`;
`standards/STANDARDS.md:57`; `standards/open-evolutions.md:13`.

**Verified problem — a trigger nothing reads.** `audit-review-history.md:32-39` mandates resolving each
row's **rule** citation against the current standard, and nothing else. `documentation.md:150` defines
the Re-check trigger as "the condition that ends the deviation, stated so a reader can tell whether it
has already fired" — with no rule telling anyone to evaluate it, and none requiring a cited **evidence
id** to resolve. Both failure modes are live: `WhatGroup/docs/ARCHITECTURE.md:349` carries a row whose
trigger fired on 2026-08-06 and is still open, and `AbsorbTracker/docs/ARCHITECTURE.md:354-357` cites
three audit ids (`AT-A-10`, `AT-A-03`, `AT-A-09`) that appear in no bundle.

**Verified problem — the inventory.** `LibKa0s/LibKa0s.xml` lists **fourteen** `Script` entries.
`library-stack.md:70` says "ten LibStub majors across **thirteen** files", `:82` gives the Options row
`Options.lua, OptionsWidgets.lua, OptionsScroll.lua`, and `standards/STANDARDS.md:57` and
`standards/open-evolutions.md:13` repeat "ten majors across thirteen files". The missing file is **`OptionsCompose.lua`** — which is where `C01` lives. The
section describing the library's module set does not know about the file that broke nine repositories'
dropdowns.

**Change.** Add a third MUST to `audit-review-history`: evaluate each row's trigger, and resolve each
cited evidence id. Correct `:70` to fourteen, add `OptionsCompose.lua` to the Options row at `:82`, and
sweep the two restatements.

**Closes:** `LIBKA0S-A-14`, and `C25`'s standards half. **Unblocks:** `C14`, which is uncheckable until
the register has a rule that reads triggers. **Adoption cost:** the `C14` register sweeps, which now
have something to check against.

---

## M1-STD-16 · Version rollup

Last, after every other Group B item. Bump `STANDARDS.md`'s version and date, roll the changelog, and
re-issue the context pack. `M1-LK-14` moves the nine addons' and the library's standards pointers to
whatever this lands as; do not cut `M1-LK-14` before this.

---

# Group C — the `wow-addon` plugin

Path: `/mnt/d/Profile/Users/Tushar/Documents/GIT/wow-addon`. Six items, all in the two agent
definitions and three commands. None blocks an addon milestone; all six exist so the next cycle costs
less than this one did.

---

## M1-WA-01 · `review.md` gains a cross-addon, same-session pass

**File:** `agents/review.md` (321 lines).

**Verified problem.** The entire checklist is per-addon. Its only cross-repo line is "`## Interface:`
value inconsistent with sibling addons". Nothing asks what happens when all nine load together, which
is the collection's stated deployment — and the one live cross-addon fault in this cycle (`C02`,
process-global widget registry) was found by a lens held above the bundles, not by any of the twenty
passes.

**Change.** Add a cross-addon section covering the four collision classes, all of which were run for
this bundle and are currently clean: slash-token distinctness, vendored LibKa0s minors identical across
consumers (LibStub's same-minor-different-bytes hazard), vendored payload byte-identity across the nine,
and `## Interface:` uniformity. Record what "clean" looks like so the next pass can diff rather than
re-derive.

---

## M1-WA-02 · The census commands count the whole tracked set

**Files:** `agents/review.md`, `agents/standards-audit.md`.

**Verified problem.** `C22` claims eleven files over `layout-§1`'s cap across five repos. `wc -l` over
`git ls-files '*.lua'` excluding `libs/` and `tests/_kit/` finds **eighteen**, in three repos, and two
of the five named have none. Different passes counted different denominators: `MULTIMETERS-R-08` scopes
itself to "seven **shipped** files" while `LIBKA0S-A-03` and `CONSUMABLEMASTER-A-06` both counted test
files. The same split shows in `C10`, where the per-repo line-ending counts are 21 (MultiMeters), 9
(LootHistory), 8 (KickCD), 7 (ConsumableMaster), 6 (WhatGroup), 5 (PanelMaster), 4 (BankLedger), 2
(AbsorbTracker), 2 (PrettyChat) and 7 (LibKa0s), enumerated in some and given as "repo working tree" in
others.

**Change.** Both agents state the exact command and denominator for every census they run, and report
the count with the command beside it. **Depends on `M1-STD-08`** for the cap's scope, so the command
matches the rule.

---

## M1-WA-03 · `revendor-libka0s` checks for a contract change, not only a version change

**File:** `commands/revendor-libka0s.md`.

**Verified problem.** `M1-LK-02` changes when `O.LSMValues` is called — declaration time rather than
render time — without changing any signature. A re-vendor reports per-file LibStub minors and two
diffs, none of which can show that. MultiMeters would take the new payload, keep
`settings/Schema.lua:670`, pass every suite, and freeze its media lists at file load.

**Change.** The command reads the tag's API document for each moved minor and reports **behavioural**
changes to `__Attach*` contracts as adoption blockers, not as candidates. A host-supplied member whose
call site moves is the shape to look for.

---

## M1-WA-04 · `sync-docs` reads code comments against the tree

**File:** `commands/sync-docs.md`.

**Verified problem.** `C19` is thirteen findings across eight repos: comments and rationales naming
functions, files and hazards that no longer exist — `PanelMaster/settings/OptionsSetup.lua:190-195`
names `Sl:CliResetAll`, which no `.lua` file defines; `AbsorbTracker/core/AbsorbTracker.lua:69` cites a
re-entrancy hazard `Options.lua:838-844` now documents as guarded; `MultiMeters/tests/test_vendor_sync.lua:14`
quotes a LibKa0s version three majors old. The house style deliberately carries `file:line` citations
and design arguments in prose, and nothing verifies them, so they rot silently.

**Change.** `sync-docs` already has a comment-citation gate in its description; extend it to resolve a
named symbol as well as a named path, and to report rather than rewrite.

**Note the ordering.** `M1-LK-02` makes three of `C19`'s comments stale by design — AbsorbTracker's at
`settings/Appearance.lua:121-129` says "delete this the re-vendor after the fix lands". Run the sweep
**after** the adoption wave, not before.

---

## M1-WA-05 · `new-addon` scaffolds a non-English-client smoke step

**Files:** `commands/new-addon.md`, and the smoke-test scaffold it writes.

**Verified problem.** Six of nine `docs/smoke-tests.md` files carry no non-English-client step, and the
two addons whose code is most locale-sensitive are among them. LootHistory has none although
`core/Compat.lua:188-195` defines four English wordings as the fallback when the client leaves
`ITEM_ACCOUNTBOUND*` nil, reached at `:230-231`, and the same file calls the tooltip "the ONLY witness"
for items whose bind type lies. PrettyChat has none in 797 lines, and its whole function is overwriting
localised `_G` chat format strings. Every headless case for those paths asserts against enUS mock
globals — `LootHistory/tests/test_compat.lua:65-66` passes the literals `"Auction House"` and
`"Auction won: …"`.

**Change.** The scaffold ships one locale step by default, and the audit agent reports its absence where
`core/Compat.lua` or a module reads a localised global.

---

## M1-WA-06 · The standard and the plugin enter the audit rotation

**Files:** `ADDONS.md` (or wherever the rotation is declared), `commands/standards-audit`.

**Verified problem.** `WowAddonStandards` and `wow-addon` received neither a review nor an audit on
2026-09-07, and a `find` over both returns no bundle of any date. Between them they hold
`agents/review.md` (321 lines) and `AUDIT.md` (515 lines) — the two documents all twenty passes ran on.
This cycle produced six internal contradictions in the standard (`M1-STD-04` through `M1-STD-09`), all
of them found by reading the sections against the addons rather than by auditing the sections. That is
a slow way to find a contradiction in a 25-section document.

**Change.** Give both repositories a lane. They are docs-only, so the checklist is small: internal
consistency between MUSTs, every cross-reference resolves, every worked example still matches the
repository it cites, and the module inventories match the repositories they describe (`M1-STD-15` is one
of those, and it went unnoticed for at least one release).

---

# Surfaces that ALREADY EXIST and are merely unadopted

**This section exists to stop the plan misrouting.** Six things in the ledger read as library gaps and
are not: the surface is published, vendored in all nine consumers today at v1.25.0, and documented. The
work is adoption, and it is **addon-side**. Scheduling any of these as upstream work would put a
library release in front of a change that needs no library release at all.

| Surface | Where it lives, today, in the vendored payload | Who has not adopted it | Cluster it is filed under |
|---|---|---|---|
| `O.SetRenderer(ctx, fn)` | `LibKa0s/Options.lua:695`, with the Blizzard-sidebar combat refusal inline at `:700-716` | AbsorbTracker has **zero** callers and drives three pages off raw `ctx.panel:SetScript("OnShow", …)` — `settings/Appearance.lua:320`, `General.lua:283`, `Profiles.lua:57`. KickCD (Profiles, Spells) and MultiMeters (Profiles) each keep pages off it too. | `CX03`, `ABSORBTRACKER-R-04` |
| `O.BuildLandingPage(ctx, spec)` | `LibKa0s/OptionsWidgets.lua:1288`, whose `:323` sets the `OnRelease` that hides the logo texture | PrettyChat hand-copied the renderer at `settings/Panel.lua:646-721` and omitted the `OnRelease`, so a 300px logo rides AceGUI's pooled `SimpleGroup` into the next widget. **`C07` does not wait on any upstream item** — the surface is in the v1.25.0 payload PrettyChat already vendors. | `C07`, `PRETTYCHAT-R-02` |
| `lib.ICONS` / `lib.Icon` | `LibKa0s/Media.lua:92` and `:202` | Roughly thirty marks published; PrettyChat carries 93 hard-coded `Interface\` paths, LootHistory 19, BankLedger 17. Most are Blizzard chrome the catalog has no equivalent for, so the adoption question is *which* paths the catalog is meant to replace — not a missing surface. | `CX08` |
| `LibKa0s-Pool-1.0` | `LibKa0s/Pool.lua`, minor 3 | Four consumers use it (`BankLedger`, `KickCD`, `LootHistory`, `MultiMeters`, via `core/PoolSetup.lua`). The **library itself** does not — `M1-LK-03` is LibKa0s adopting its own published pool. | `C23` |
| `lib.MakeCloseButton`'s third argument | `LibKa0s/Core.lua:234` | Eight consumers wrap it correctly. BankLedger declines, with written reasoning at `core/CoreSetup.lua:117-129`. The argument is not missing; the standard's MUST and MAY disagree about the decline (`M1-STD-04`). | `CX06` |
| `O.MASTER_GROUP` | `LibKa0s/OptionsCompose.lua:189`, published on the instance by `__AttachCompose` | `WhatGroup/settings/Panel.lua:285` hardcodes `["Master controls"]` instead. One line, addon-side. | `WHATGROUP-R-04` |

The one item in the ledger that reads as an adoption gap and is genuinely **not addressable by
adoption** is `CX02`. A published no-op surface would have to ship in the payload that is by definition
absent on the path the stub exists for. `M1-LK-09` moves that work kit-side instead.

---

# Recommended not to do

Three items in this milestone's inbox cost more than they return, and one is filed against the wrong
repository. Each is listed so the decision is recorded rather than re-argued next cycle.

**`CX06` — rebinding `MakeCloseButton` inside `LibKa0s-Core-1.0`.** Payoff is roughly 24 lines across
eight wrappers. Cost is a signature change to a surface all nine consumers vendor, forcing a re-vendor
wave for cosmetics — and it is contradicted by the library's own reasoning at `LibKa0s/Media.lua:14-20`,
which records that `...` carries the addon folder name only for a file the TOC loads directly. If the
wrappers must go, the shape is a one-time `lib.SetHost(addonName)`, not inference. The cheap close is
`M1-STD-04` plus one register row in BankLedger.

**`C22`'s splits, pending `M1-STD-08`.** This is a MultiMeters problem: seven source files and seven
test files, and MultiMeters is also the repo carrying `C04`, the feign-trace subsystem, in `modules/`.
Splitting `settings/Schema.lua` (3069) and `modules/Window.lua` (2644) is the largest mechanical churn
in the whole plan, has no player-visible payoff, and collides head-on with the one cluster in that repo
that does. Defer past everything; if ever, only after `C04` lands.
`PrettyChat/GlobalStrings/GlobalStrings.lua` at 23,842 lines is generated, unloaded and
`.pkgmeta`-ignored, and must be exempted by rule rather than split — which is `M1-STD-08`'s job.

**Backfilling `C08`'s missing `ANALYSIS.md` files.** 93 frozen dated bundles, 35 without one. Writing
an analysis today into a bundle stamped in August is fabricating a record. Fix forward: the next run
writes one, and the gap is noted once.

**Renaming the `minimise` icon key.** Covered at `M1-LK-11`. The key is public, the path is derived
from it, and the file on disk is `minimise.tga` in ten trees. Fix the prose and the chat strings; leave
the key.

---

# The ordering constraint

What has to be tagged and re-vendored before which addon milestone. Everything below is a dependency,
not a preference.

## Inside Milestone 1

```
M1-LK-00  (renormalise two LF files)  ── before EITHER tag is cut
     │
     ├── M1-LK-01 (the four red cases) ── before M1-LK-02 touches OptionsCompose.lua
     │        │
     │        └── M1-LK-02 ──┐
     │                       ├── tag v1.26.0 (M1-LK-04)
     │        M1-LK-03 ──────┘   (if ready; must not delay M1-LK-02)
     │
     └── M1-LK-05 … M1-LK-14 ── tag v1.27.0 (M1-LK-15)

M1-STD-10 ──→ M1-LK-05   (no rule to cite until the widget-registry MUST exists)
M1-STD-12 ──→ M1-LK-11   (so the widened word list is the section's, not a second private one)
M1-STD-08 ──→ M1-WA-02   (so the census command matches the cap's scope)
M1-LK-10  ──→ M1-STD-13  (§7 cites a gate that has to exist first)
M1-LK-12  ──→ M1-STD-01  (LibKa0s pilots the .luacheckrc shape before ten repos take it)
M1-STD-16 ──→ M1-LK-14   (the pointer moves to the version the rollup lands as)
M1-STD-16 ── LAST in Group B, after M1-STD-01 … M1-STD-15
```

So **Group B leads Group A on three items** — `M1-STD-10` → `M1-LK-05`, `M1-STD-12` → `M1-LK-11`,
`M1-STD-16` → `M1-LK-14` — **and follows it on two**: `M1-LK-10` → `M1-STD-13` and `M1-LK-12` →
`M1-STD-01`. The fourth arrow above, `M1-STD-08` → `M1-WA-02`, is Group B leading **Group C**, not Group
A; `04_EXECUTION_PLAN.md` states the same split in its own numbering. The only thing that is
unconditionally parallel from day one is the addon work listed at the end of this section.

## Milestone 3 — adoption of v1.26.0

Cut v1.26.0, then re-vendor in this order. The order matters; it is not alphabetical.

1. **KickCD — re-vendor only, no code change.** Eight live dropdowns start working:
   `settings/Castbar.lua:346`, `:481`, `:503`, `:514`, `:536`, `settings/Icons.lua:207`, `:258`,
   `settings/Label.lua:184`. This is the proof the fix landed, and it is the only consumer whose
   behaviour visibly changes on the re-vendor alone. Verify in client: `/kcd config` → Icons, Label and
   Castbar dropdowns list faces, borders and textures; `/dump LibStub("LibKa0s-Options-1.0").MODULES.OptionsCompose`
   reports 3.
2. **MultiMeters — re-vendor AND revert `settings/Schema.lua:670` to `C.LSMValues = lsmValues`, in the
   same commit.** Non-optional. Without it the composed rows take a table frozen at file load, silently.
3. **AbsorbTracker and ConsumableMaster — re-vendor, then delete the workarounds.** AbsorbTracker:
   `settings/Appearance.lua:114-137` plus its three call sites at `:181`, `:237`, `:257`.
   ConsumableMaster: `settings/MacroBar.lua:121-123` plus the three row overrides at `:269`, `:337`,
   `:454`; close LibKa0s issue #15, which the comment at `:118` names.
4. **BankLedger, LootHistory, PanelMaster, PrettyChat, WhatGroup — re-vendor only.** They consume
   `MasterControls` and `ColorPair`, no media composer. Nothing moves.

Because `OptionsCompose.lua:32-35` resolves the highest compose minor present in the session, step 1
alone repairs every consumer in a live client. Steps 2–4 are still required — a session with only the
stale copies loaded is back to the defect — but the wave does **not** have to be atomic, and step 1 can
be verified in game before step 2 opens.

## Milestone 4 — adoption of v1.27.0

One re-vendor wave in all nine, carrying both payloads. Serialise **inside** LibKa0s before cutting it:
three items land on `Options.lua` (`M1-LK-05`, `M1-LK-09`'s manifest, `M1-LK-14`) and **three** on
`OptionsWidgets.lua` — `M1-LK-03` if it slipped, `M1-LK-06`, and `M1-LK-13`, whose printer change is to
that file's `local print = d.print or function() end` at `:696`. Do `Options.lua`, then
`OptionsWidgets.lua`, then `testkit/`.

The serialisation point **inside each addon** is `settings/OptionsSetup.lua`. `CX02`'s parity case,
`CX03`'s `SetRenderer` stub line, `C07`'s `BuildLandingPage` no-op and `M1-LK-05`'s patch call site all
land in that one file. One lane owner per repo at a time; never two agents in it.

`M1-LK-05` additionally requires the multi-addon in-client smoke test described in that item, and the
five `core/LSMPatch.lua` deletions afterwards, in five separate commits, AbsorbTracker's last.

## What needs no upstream item at all

**None of these has an upstream dependency.** Every one could start before either tag exists, and this
section originally argued that scheduling them behind Milestone 1 would be a mistake. **The owner
decided on 2026-09-07 that they wait for M1 anyway** (`00_OVERVIEW.md` decision 3), so they are M2 and
M2 follows M1. The list is kept as the record of what is *technically* unblocked, which is what a future
reader needs in order to reorder the plan if M1 stalls:

- `C03` — BankLedger `defaults/Global.lua:14` + `core/Database.lua:15-21`, and ConsumableMaster
  `core/Database.lua:65-90`. Fix the fakes first (`BANKLEDGER-R-03`, `CONSUMABLEMASTER-R-14`); both
  defects are pinned by cases that cannot go red. Highest blast radius in the plan, because a wrong fix
  corrupts a real ledger.
- `C04` — the MultiMeters feign-trace subsystem, eight findings, entirely inside that repo.
- `C05` — `LootHistory/core/Database.lua:748-754`, a pure function, provable headless.
- `C06` and `C07` — PrettyChat. `C07` in particular: the cluster's ordering puts it behind the library
  wave, and that is wrong — `O.BuildLandingPage` is already at `OptionsWidgets.lua:1288` in the v1.25.0
  payload PrettyChat vendors today.
- `CX03` — AbsorbTracker, KickCD, MultiMeters. Adoption of a shipped surface.
- `C11` — the `.pkgmeta` omissions. The template line is `M1-STD-09`, and none of the repo-local entries
  wait on it. The **16.3M of tracked `media/screenshots`** that KickCD, LootHistory, AbsorbTracker and
  WhatGroup ship do not need a standards amendment to stop shipping. AbsorbTracker's 2.8M of
  `.superpowers` review diffs are **untracked and gitignored**, reach no packager clone, and are listed
  under `packaging.md:28`'s strong form rather than because they ship — the same test that rejected the
  identical claim in three other repositories.
- The in-client-only set — `C29`'s combat transitions, `WhatGroup/settings/Schema.lua:577`'s
  `StaticPopupDialogs` assignment, `ConsumableMaster/settings/Panel.lua:866-867`'s unguarded
  `RegisterAddOnCategory` — which should be batched into one client session rather than spread across
  milestones, because none of them can be proved headless and each costs a login to check.

## What must wait, and for what

| Addon work | Waits on | Why |
|---|---|---|
| `C02` — delete five `core/LSMPatch.lua` copies | `M1-STD-10`, then `M1-LK-05` in v1.27.0 | No rule to cite, and no library surface to call. |
| `C08` — the record sweep in ten repos | `M1-STD-07` | Until `automated-tests-§4` and `documentation-§3` agree, nobody can write the file correctly. |
| `C10` — the working-tree sweeps | `M1-LK-00` for the library slice; `M1-LK-10` + `M1-STD-13` for the gate | Sweeping before the gate exists means sweeping again next cycle. |
| `C12` — geometry cases | `M1-LK-08` kit 15, then kit 16 | The mock cannot express the assertion today. |
| `C17` — the spelling sweeps | `M1-STD-12` | So the gate that follows reads the section's list. |
| `C22` — any split | `M1-STD-08` | The cap's scope is undefined in three directions; most of `C22` may not be a breach. |
| `CX04` — TOC annotations | `M1-STD-02` | Eight one-liners, not nine TOCs — but only after the denominator is settled. |
| `CX05` — `.luacheckrc` narrowing | `M1-LK-12`, then `M1-STD-01` | Prove the config shape in one repo before ten take it. |
| `C14`, `C15`, `C16` — register and doc-structure sweeps | `M1-STD-03`, `M1-STD-15` | Both change what a correct register looks like. |
| `C19` — the comment sweep | Milestone 3 and 4 adoption | `M1-LK-02` makes three of its comments stale by design; sweeping first means sweeping twice. |

## Milestone 1 exit criteria

- `git ls-files --eol` in LibKa0s reports zero `w/lf` or `w/mixed` files under `attr eol=crlf` — **all
  seven repaired**, not the two in the payload — and `diff -r LibKa0s <Addon>/libs/LibKa0s` is byte-empty
  for the first consumer re-vendored.
- `lua tests/run.lua` in LibKa0s is green, with the four `M1-LK-01` cases present and having been seen
  **red** before `M1-LK-02` landed.
- `docs/api/Options/version-14.13.3.3-docs.md` exists — `tests/test_versioning.lua:159-181` derives the
  path from live `lib.MODULES` and stays red until it does, so this is enforced rather than remembered.
- Tag `v1.26.0` carries a release bundle naming it. `v1.24.0` does not, which is `LIBKA0S-A-05`.
- `WowAddonStandards` version and date bumped, changelog rolled, context pack re-issued.
- Every `M1-STD-*` item's ripple swept: no document outside an amended section still restates the old
  text.
