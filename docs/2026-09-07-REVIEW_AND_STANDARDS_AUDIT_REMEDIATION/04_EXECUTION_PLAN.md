# 04 — Execution Plan

**100 work items across five milestones, ordered by dependency and nothing else.**

> **Nothing in this plan has been executed.** No item below has been started. No branch exists, no tag
> has been cut, no payload has been copied, no `.pkgmeta` line has been added, no test has been written.
> Every "add", "delete" and "re-vendor" is an instruction to a future change. The suites named here are
> green today at the figures the per-repo bundles recorded, and this document does not move them.

See `03_SPEC.md` for what each item must achieve, `02_UPSTREAM_CHANGES.md` for the upstream rationale
and blast radius, `01_CONSOLIDATED_FINDINGS.md` for the findings themselves.

**There are no dates in this document.** Milestones order work; they do not schedule it.

---

## Milestone map

| M | Name | Items | Repos touched | Depends on |
|---|---|---|---|---|
| **M1** | Upstream — the library, the standard, the plugin | 38 | LibKa0s, WowAddonStandards, wow-addon | nothing |
| **M2** | The defects that need no upstream anything | 27 | PrettyChat, BankLedger, ConsumableMaster, MultiMeters, LootHistory, AbsorbTracker, KickCD, WhatGroup, PanelMaster | **M1 complete** — by the owner's decision of 2026-09-07, not by any technical dependency |
| **M3** | Adoption of v1.26.0 | 5 | all nine addons | M1 Group A through `M1-LK-04` |
| **M4** | Adoption of v1.27.0, and the compliance the rulings unblock | 26 | all nine addons | M1 complete, M3 |
| **M5** | The record and documentation tail | 10 | all ten repos | M2, M3, M4 |

**The rule this plan is built on:** every change to LibKa0s, WowAddonStandards or the `wow-addon`
plugin is in M1. No item in M2 or later touches any of the three except as a re-vendor consumer.

**M2 runs after M1, by decision rather than by dependency.** Not one of its items waits on a tag: it
contains every reachable defect in the collection — the two migration runners, the chat-format writer,
the pooled-logo leak, the feign trace — and it could technically start the hour this plan is approved.
The owner decided on 2026-09-07 that it waits for M1 to complete, and the plan is written that way.

**What that costs, stated once so nobody rediscovers it in week three.** The five High findings and the
one Critical-adjacent player-facing defects all sit in M2, and they now wait behind 38 upstream items
across three repositories. M1's own long pole is `M1-LK-07`, the test-kit runner, which is the single
largest item in the bundle. The upside the decision buys is real and is why it is defensible: every M2
repository is a repository M3 and M4 will re-vendor, and a serial order means no addon is opened twice
by two lanes that do not know about each other — the failure mode that the parallel reading trades
against. If M1 slips, the reachable defects slip with it; that is the trade, and it is the owner's.

Two consequences follow mechanically. `M2-23`'s issue reconciliation now lands after the standard is
amended rather than before it, which is strictly better — the dispositions it writes cite rules that
exist. And `C07`'s library surface has been in the payload PrettyChat vendors since before v1.25.0, so
`M2-02` never needed M1 regardless; it is now simply later.

**`⚠` marks an item carrying at least one check that cannot be made out of game.** There are
**eighteen** — seventeen in sessions 1 to 5 and `M5-08`, which owns session 6 — and every one of them
names its smoke check and the session it belongs to; the batched sessions are listed under
"In-client smoke sessions" near the end. **Every `⚠` item appears in one of the six sessions in
`06_SMOKE_TESTS.md`, and every session step that is the *reason* for a login belongs to a `⚠` item.** The
reverse does not hold, deliberately: a session also picks up checks on items that can be proved headless,
because the operator is already in the client — those are marked *(opportunistic)* there and are never a
reason to schedule a login. An item that schedules a load-bearing in-client step and carries no `⚠` is an
item an operator filtering on `⚠` to plan client time will miss, and there are none.

---

## Standing verification, every item

Unless an item says otherwise, "verified" means all of this in the repository touched:

```
luacheck .                                            # 0 warnings / 0 errors
lua tests/run.lua                                     # 0 failed
git status --porcelain                                # only the intended paths
```

and, where the item moves a measured figure:

```
tests/_kit/run-automated-tests.sh --no-bundle         # four suites, writes nothing
```

Where a case count moves, the item states the expected delta and `docs/test-cases.md` plus the README
`[tests]` badge move in the **same commit** —
`lua tests/run.lua --list > /tmp/list && diff <(tr -d '\r' < /tmp/list) <(tr -d '\r' < docs/test-cases.md)`
must be empty, CR-normalised on both sides because the runner's output is CRLF in most of these repos.

**Copy commands out of the rendered page, not the raw markdown.** Inside these tables `\|` is GFM
escaping and renders as a literal `|`, so the *rendered* `grep -riE 'colour|grey'` is a correct ERE.
Copied from source you get a pattern matching the single string `colour|grey`, which appears nowhere and
can never fire. Strip the backslashes.

**Where an item carries a `Smoke, session N` line, that step is written into the owning addon's
`docs/smoke-tests.md` in the same commit as the change it proves.** `06_SMOKE_TESTS.md` is a frozen,
dated bundle in a thirteenth repository; a check that lives only here is runnable next cycle only by
someone who knows this directory exists. The three genuinely new checks — PrettyChat's pooled-logo leak
crossing into another addon's panel, the late-registration media check that is the only signal for the
`__AttachCompose` contract change, and the five-addon load-order sweep — are the ones this rule is for.

**Every "Verified by" command is shown failing before it is accepted.** Plant the violation, run the
command, watch it go red, revert, watch it go green. This is not ceremony: `C21` is nine cases that stay
green under the change they exist to catch, and `LIBKA0S-A-01d` is 764 green cases that missed the
collection's only Critical. A verification that has only ever been green has proved nothing.

---

# M1 — Upstream

Every change to LibKa0s, WowAddonStandards and the plugin. Three groups. **Group B leads Group A on
three items and follows it on two**, so they interleave rather than running in sequence; Group C is
independent of both except `M1-WA-02`.

## M1 · Group A — LibKa0s

Path: `/mnt/d/Profile/Users/Tushar/Documents/GIT/LibKa0s`. Two tags. `M1-LK-00` … `M1-LK-04` ship as
**v1.26.0**; `M1-LK-05` … `M1-LK-14` ship as **v1.27.0**, cut by `M1-LK-15`.

| ID | Repo | What changes | Verified by | Depends on | Effort |
|---|---|---|---|---|---|
| **M1-LK-00** | LibKa0s | `rm` plus `git checkout --` on **all seven** working-tree LF files under `attr text=auto eol=crlf`: `LibKa0s/DebugLog.lua`, `LibKa0s/Pool.lua` (the shipped payload), `tests/test_debuglog.lua`, `tests/test_pool.lua`, `docs/api/Options/version-8.7.3-docs.md`, `docs/api/Options/version-9.7.3-docs.md`, `docs/api/testkit/version-12-docs.md`. The index is already correct for all seven, so no commit is needed and no minor moves. **First, before either tag** — and before `M1-LK-10` widens the gate, which would otherwise turn the LibKa0s suite red on the five non-payload files with no item to repair them. | `git ls-files --eol \| grep -E 'w/(lf\|mixed)'` lists only the two `.sh` files under `attr eol=lf`. Then `diff -r LibKa0s ../AbsorbTracker/libs/LibKa0s` is byte-empty — a check that has never passed in this collection. | — | S |
| **M1-LK-01** | LibKa0s | Write four cases in `tests/test_options_compose.lua`: `type(rows[n].values()) == "table"` and non-empty for `FontGroup`, `BorderGroup`, `BarGroup`, plus one asserting a host-supplied table-returning `LSMValues` is rejected. **Written red, before `M1-LK-02` touches anything.** | `lua tests/run.lua` reports exactly 4 new failures and no other change against today's 764. | M1-LK-00 | S |
| **M1-LK-02** | LibKa0s | `LibKa0s/OptionsCompose.lua:231`, `:275`, `:304`: `values = O.LSMValues("font"\|"border"\|"statusbar")`, dropping the outer closure. `COMPOSE_MINOR` (`:29`) 2 → 3. Document the `__AttachCompose` contract at `:181`: a host-supplied `O.LSMValues` MUST return a function. Write `docs/api/Options/version-14.13.3.3-docs.md`. | `lua tests/run.lua` → 768 passed, 0 failed. `grep -c 'function() return O.LSMValues' LibKa0s/OptionsCompose.lua` → 0. `tests/test_versioning.lua` is green, which it cannot be until the API document exists. | M1-LK-01 | S |
| **M1-LK-03** | LibKa0s | `TabStrip` (`OptionsWidgets.lua:1050-1072`) acquires buttons and the content panel from per-`ctx` `LibKa0s-Pool-1.0` pools; `makeTab` (`:942`) splits into `newTabButton` + `dressTab` with `OnClick` re-set per dress. `WIDGETS_MINOR` (`:15`) 13 → 14, with its API document. | A new case selecting each tab twice asserts zero `CreateFrame` calls on the second pass, counted through the mock. Red against today's code. | M1-LK-00 | M |
| **M1-LK-04** | LibKa0s | **Cut v1.26.0.** `docs/releasing.md` steps 1–7 verbatim. M3 cannot start without it. | `git tag \| grep v1.26.0`; the release bundle under `docs/automated-tests/` names 1.26.0 in its manifest — which `v1.24.0` does not, and that is `LIBKA0S-A-05`. | M1-LK-02, and M1-LK-03 **only if ready** — it must not delay this tag | S |
| **M1-LK-05** | LibKa0s | New `lib.__PatchLSM30Border()` on `LibKa0s-Options-1.0`: lib-level, idempotent behind `lib.__lsmBorderPatched`. Options `MINOR` (`Options.lua:24`) 14 → 15, with its API document. | A case calls it twice and asserts the second is a no-op. `grep -n '__lsmBorderPatched' LibKa0s/Options.lua` resolves. Full proof is `M4-03`, in client. | M1-STD-10 (no rule to cite until it exists), M1-LK-04 | M |
| **M1-LK-06** | LibKa0s | Add `lib.STRINGS.DEAD_BUTTON`; `makeBtn` (`OptionsWidgets.lua:1313-1319`) reports once at build time for a handler-less button and renders anyway, matching `EMPTY_DROPDOWN` at `:1443`. | A case asserts one report and one rendered button. | M1-LK-04 | S |
| **M1-LK-07** | LibKa0s | `testkit/run-automated-tests.sh`: widen the pass regex at `:195` to span `, N skipped`; add `suites.tests.skipped` to the manifest; render `:388`'s Version cell as `version → release` when `manifest.release` is set; move the four-checkpoint lead-in out of the file-absent branch at `:414-432` so it rewrites an existing `RESULTS.md` above a matching header, rows preserved. **And emit the two things `automated-tests.md:221-224` MUSTs and the runner has never written**: the complexity watch list, as the section's two tables — warned functions (Function / CCN / Location / Disposition) and files by `layout-§1` band — generated from the run's own `lizard` output with the Disposition column carried forward from the previous file where the entry is unchanged and left blank where it is new; and one standing section per suite, generated from the same manifest. This is what `M1-STD-07` decides the shape of and **the reason `C08` is stale in ten repositories**: today `:388`-`:437` writes one table row plus a fixed lead-in and nothing else, so the mandated narrative has no producer. `Kit.VERSION` (`testkit/framework.lua:20`) 14 → 15, with `docs/api/testkit/version-15-docs.md`. | A scratch suite with one `Kit.skip` run through `tests/_kit/run-automated-tests.sh --no-bundle` prints a non-zero skipped figure and a total that includes it. `jq .suites.tests.skipped` on the newest bundle resolves. **Run in MultiMeters, the watch list it writes names all 23 warned functions with their measured CCN**, and a second run with one entry's disposition hand-filled preserves that disposition and nothing else. | M1-LK-04, M1-STD-07 | L |
| **M1-LK-08** | LibKa0s | `testkit/mock_base.lua`: add `SetAtlas(name, useAtlasSize)` writing a height from a kit-published atlas table, plus opt-in `f:__setGeom(w, h)`. **Additive only — `GetHeight` still returns 0 at `:97`.** The flip is a later kit 16, deliberately not in this plan's scope. | Every one of the ten repositories' pass counts is **unchanged** after adoption. An unchanged count is the whole point of an additive mock change. | M1-LK-07 | M |
| **M1-LK-09** | LibKa0s | `testkit/framework.lua`: add `Kit.assertSurfaceParity(stub, majorName)` reporting all divergences in one message; publish a machine-readable member list under `docs/api/` derived from live `lib.MODULES`. Kit 15. | A scratch call with a stub missing one member fails and names it. `grep -n 'assertSurfaceParity' testkit/framework.lua` resolves. | M1-LK-07 | M |
| **M1-LK-10** | LibKa0s | Move `tests/test_eol.lua` into `testkit/` and widen `trackedFiles()` from `:29`'s `BUNDLES = "docs/automated-tests"` to the whole `git ls-files` set, keeping the NUL guard. Kit 15. | Converting one tracked CRLF file to LF turns the suite red; reverting turns it green. Today the same mutation is invisible to it. | M1-LK-07, M1-LK-00 | S |
| **M1-LK-11** | LibKa0s | `tests/test_prose.lua:113`: replace the six-substring `BRITISH` list with the canonical list `M1-STD-12` publishes. Sweep `LibKa0s/Perf.lua`'s five player-facing sites — `CANCELLED` at `:948` and `:1063`, `unlabelled` at `:723`, `:864` and `:1029` (`localization.md:139`'s Use/Never table carries `labelled` → `labeled`) — and the authored comments. **Do not rename `lib.ICONS`'s `minimise` key** — `lib.Icon` derives the path from it and `minimise.tga` is the file on disk in ten vendored trees. | The widened gate is red against today's `Perf.lua` and green after the sweep. `grep -n 'minimise' LibKa0s/Media.lua` still resolves. | M1-STD-12 | S |
| **M1-LK-12** | LibKa0s | `.luacheckrc:4`: narrow `exclude_files` from `{ "tests/", "docs/" }` to `tests/_kit/`, and add a `files["tests/"]` stanza declaring the kit globals rather than widening top-level `read_globals`. **This is the pilot for `M1-STD-01` and `M4-11`** — prove the shape in one repo before nine take it. | `luacheck .` 0/0 with the 31 files under `tests/` in scope, against 18 of 49 covered today. | — | S |
| **M1-LK-13** | LibKa0s | Four library-local items: store the shell's constructed sink as `O.__print` so `OptionsWidgets.lua:696`'s `local print = d.print or function() end` stops swallowing `NO_GROUPS`/`EMPTY_DROPDOWN`/`BUTTON_FAILED`; reuse bracket slots from a high-water free list at `Perf.lua:478` and state the active-arm cost in its docstring; take `C_SpecializationInfo.GetSpecialization` before the bare global at `Perf.lua:615-618`; add one comment at `tests/run.lua:110-118` naming `Kit.assertSuiteInventory` as what holds the hand-typed suite list honest. | A case asserts `NO_GROUPS` reaches the shell's sink. A new active-arm allocation case sits beside the dormant one at `tests/test_perf_isolation.lua:66`, with a ceiling from three runs. | M1-LK-04 | M |
| **M1-LK-14** | LibKa0s | `CLAUDE.md:3` and `README.md:3`: standards pointer v2.28.0 → whatever version `M1-STD-16` lands as. `docs/releasing.md`: add the pointer check to the step order, make the four-suite bundle a hard precondition of the tag, and have the runner refuse to stamp a dirty tree as a release — `20260903-161751` records `dirty: true` at sha `895cdf4`. | `grep -n 'v2\.' CLAUDE.md README.md` matches `head -1 ../WowAddonStandards/standards/STANDARDS.md`. | M1-STD-16 | S |
| **M1-LK-15** | LibKa0s | **Cut v1.27.0.** `docs/releasing.md` steps 1–7. Serialise the preceding items inside the library first: `Options.lua` (`M1-LK-05`, `M1-LK-09`'s manifest, `M1-LK-14`), then `OptionsWidgets.lua` (`M1-LK-03` if it slipped, `M1-LK-06`, `M1-LK-13`), then `testkit/`. | `git tag \| grep v1.27.0`; the release bundle names 1.27.0; `tests/test_versioning.lua` green, which requires an API document for Options 15, Compose 3, Widgets 14 and Kit 15. | M1-LK-05 … M1-LK-14 | S |

**Safely parallel inside Group A:** `M1-LK-03`, `M1-LK-06`, `M1-LK-12` and `M1-LK-13` touch
disjoint files and can run concurrently; `M1-LK-07` joins them once `M1-STD-07` has ruled on which half
of the record is authored, and it is the longest item in the group. `M1-LK-08`, `M1-LK-09` and `M1-LK-10` all land in `testkit/` and
must be serialised against each other.

## M1 · Group B — WowAddonStandards

Path: `/mnt/d/Profile/Users/Tushar/Documents/GIT/WowAddonStandards`, at v2.38.0 (2026-09-02). New
subsections are **appended**, never inserted, so no `filename-§N` renumbers.

**Two items reverse a disposition and lead the group**, because a plan that ships `CX04` and `CX05` as
triaged is worse than a plan that ships nothing: between them they would put roughly 320 files of work
into ten repositories to satisfy readings the standard's own text does not carry.

**What a `grep` in the *Verified by* column of this group proves, and what it does not.** Fifteen of the
sixteen items below are verified by grepping the amended file for a word the amendment introduces. That is
a **presence** check: it goes green the instant the token is typed, whatever the text around it says, so
it is the weakest verification in this plan and it is stated as such rather than dressed up. Two things
carry the real weight. Each amendment **MUST** state, in its own text, the case that made it necessary —
the repository and the `file:line` that the old wording got wrong — so a reader can check the rule against
the instance it was written for. And `M5-06` re-runs `/wow-addon:standards-audit` in all ten repositories
against the amended standard: a rule that reads well and still files the same row has not landed.
`M1-STD-16`'s ripple sweep is where a half-applied amendment shows up.

| ID | Repo | What changes | Verified by | Depends on | Effort |
|---|---|---|---|---|---|
| **M1-STD-01** | WowAddonStandards | `lint.md:11`'s template narrows `exclude_files` to `tests/_kit/` and gains a `files["tests/"]` stanza; `lint.md:32`'s normative sentence is rewritten to match. **Reverses `CX05`'s `per-addon` disposition** — as filed it asks ten repos to violate the template they all follow exactly. | `grep -n 'tests/_kit/' standards/standards/lint.md` resolves and no template line excludes bare `tests/`. | M1-LK-12 (the shape is proved in one repo first) | S |
| **M1-STD-02** | WowAddonStandards | `toc-file.md`: state that `§5:144`'s MUST binds only load-bearing positions and that `:147`'s conventional annotation is a per-group SHOULD. **Reverses `CX04`'s reading** — measured against `:144`'s own denominator this is eight one-line additions across three TOCs, not nine TOC files of work. | `grep -n 'load-bearing' standards/standards/toc-file.md` resolves with the denominator stated. | — | S |
| **M1-STD-03** | WowAddonStandards | `documentation.md` `§3`: name a fourth `Verification and record` table and say whether `ARCHITECTURE.md` registers itself. Nine of nine repos already wrote that table because the three-tier MUST at `:279` is unsatisfiable for `testing.md`, `smoke-tests.md` and the five record docs `§3` itself puts outside the tier model at `:56-62`. Ripple: `NEW_ADDON.md:204`, `NEW_ADDON_CONTEXT.md:1299`, `wow-addon/commands/sync-docs.md:12`, `wow-addon/CLAUDE.md:50`, `wow-addon/agents/standards-audit.md:40`. `AUDIT.md:96` needs nothing. | `grep -rn 'Verification and record' standards/` resolves; every rippled file names four tables. | — | S |
| **M1-STD-04** | WowAddonStandards | `standalone-windows.md`: resolve `:30`'s "every close control MUST be built through that wrapper" against `:34`'s "a host MAY draw a different one on its own windows", so a reasoned decline is a terminal compliant state with a register row. | `grep -n 'MAY' standards/standards/standalone-windows.md` and the MUST no longer contradict. A fresh audit of BankLedger files no MUST row for its four title bars. | — | S |
| **M1-STD-05** | WowAddonStandards | `library-stack.md`: mark AceEvent-3.0 and AceTimer-3.0 in `§1`'s mandatory table (`:13-14`) as mandatory-when-used, or state that `§3`'s prune rule (`:39`) governs the table. PrettyChat uses neither and must currently both vendor and not vendor them; it holds a register row for the collision at `docs/ARCHITECTURE.md:230`. | `grep -n 'AceEvent' standards/standards/library-stack.md` shows the qualification. PrettyChat's row can be retired in `M5-02`. | — | S |
| **M1-STD-06** | WowAddonStandards | `line-endings.md` `§5` (`:133-135`) sanctions a clearly delimited appendix block below the canonical `.gitattributes` body for repo-specific extension-less binaries, so `§4`'s mark-every-binary MUST and `§5`'s byte-for-byte MUST stop colliding. PanelMaster's `tools/artwork/bin/realesrgan-ncnn-vulkan` (`.gitattributes:70`) is the live case, recorded at its `docs/ARCHITECTURE.md:197`. | `grep -n 'appendix' standards/standards/line-endings.md` resolves; PanelMaster's 86-line file is compliant against KickCD's canonical 81. | — | S |
| **M1-STD-07** | WowAddonStandards | Settle `automated-tests.md:222-241` against `documentation.md:68`. One MUSTs per-entry dispositions and a standing section per suite; the other calls `RESULTS.md` generated and never hand-edited. Decide which half is authored, and make the generated half producible by the runner. **This is `C08`'s actual mechanism** — ten repos are stale because nobody can write the file correctly. Re-count while there: 93 bundles, 35 without `ANALYSIS.md`, and `:245` only MUSTs one for release runs. | `grep -n 'hand-edited\|generated' standards/standards/automated-tests.md standards/standards/documentation.md` shows one consistent rule. | — | M |
| **M1-STD-08** | WowAddonStandards | `layout.md`: state whether `§1`'s 1500-line cap (`:55`) binds `tests/` — the skeleton block lists `tests/` at `:39` while `:52`'s MUST scopes *source* to the five folders that do not include it — and whether it binds generated non-shipping data and a library repo. `library-stack.md`: `§7`'s applicability block at `:175-179` promises "three lists" and carries two (`:182-193` *Applies, unchanged*, `:195-209` *Does not apply*) plus a *Substitutes* list at `:211-228` that is not an applicability list at all. Add the missing **applicability** list naming the sections the existing two omit — layout, architecture, performance, compat, anti-patterns, public-api, debug-logging, events-frames-taint, standalone-windows, naming-cheatsheet, audit-review-history, `documentation-§4` — or state a default with the two lists as exceptions. | `grep -n 'generated' standards/standards/layout.md` resolves; the third list names every section absent from the first two. | — | M |
| **M1-STD-09** | WowAddonStandards | `packaging.md`'s minimum template (`:9-24`) gains `.pkgmeta`, so it stops failing `:28`'s own strong-form MUST — every root dotfile and dot-directory present in the repo must appear in the ignore list or be justified beside it. The template already carries `.claude` and `.superpowers` at `:18-19`, so the `.pkgmeta` self-reference is the whole of this edit. Seven repos are non-compliant for having followed it; only ConsumableMaster and MultiMeters ignore `.pkgmeta` today. | `grep -n 'pkgmeta' standards/standards/packaging.md` finds it inside the template block, and the template's own ignore list satisfies `:28` read against a repo laid out to `layout.md:9-50`. | — | S |
| **M1-STD-10** | WowAddonStandards | New rule: a widget-type re-registration against AceGUI's process-global registry is a LibKa0s concern, never a per-addon one. Add anti-pattern **#76** (the list ends at #75) naming the process-global tell. `anti-patterns` #8's sanction of `RegisterWidgetType` over forking stands — the rule is about *where*, not *whether*. | `grep -n '#76' standards/standards/anti-patterns.md` resolves; `KICKCD-R-01` and `PANELMASTER-R-01` have a rule to cite. | — | S |
| **M1-STD-11** | WowAddonStandards | `options-ui`: rule on shipping composers without the Options major — `KICKCD-A-10`'s provisional register row says a library-less load registers 112 of 228 rows and asks which `§1` MUST wins. Separately narrow `§16`'s grep so it stops misclassifying an addon-wide broadcast meta row (`MultiMeters/settings/Schema.lua:1553-1566`), or have the composers expose a broadcast-meta arm. | Both `KICKCD-A-10` and `MULTIMETERS-A-12` resolve against the amended text with no addon change. | — | M |
| **M1-STD-12** | WowAddonStandards | `localization.md` `§5` publishes the canonical substring list its Use/Never table implies, and requires a mechanical gate to use it whole. LibKa0s built a private six-substring list, two entries of which are not in `§5`'s table at all, and it stays green while `CANCELLED` ships to chat. | `grep -n 'minimis\|cancelled' standards/standards/localization.md` resolves inside the published list. | — | S |
| **M1-STD-13** | WowAddonStandards | `line-endings.md` `§7` (`:362-370`) cites the vendored EOL gate rather than only supplying a command. Ten of ten repos fail this MUST today, which is what a rule with an auditor and no seam looks like. | `grep -n 'test_eol' standards/standards/line-endings.md` resolves. | M1-LK-10 (the gate has to exist to be cited) | S |
| **M1-STD-14** | WowAddonStandards | `documentation.md:237` gives `compat-layer.md`'s trigger a number, as `slash-dispatch.md` got "eight or more commands" at `:235` and `message-bus.md` got "more than ten" at `:238`. It is the only Tier 2 trigger that is pure judgment, and four repos read it four ways. | `grep -n 'Compat.lua' standards/standards/documentation.md` shows a threshold. | — | S |
| **M1-STD-15** | WowAddonStandards | Two register rules and one inventory correction. `audit-review-history.md:32-39` gains a third MUST: a row's re-check trigger is evaluated against the tree and a cited evidence id must resolve — today only the rule citation is checked, so `WhatGroup/docs/ARCHITECTURE.md:349` carries a trigger that fired on 2026-08-06 and stays open. `STANDARDS.md:57`, `library-stack.md:70` and `open-evolutions.md:13` read fourteen files, not thirteen, and `library-stack.md:82`'s Options row gains `OptionsCompose.lua` — the file where `C01` lives. | `grep -rn 'thirteen files' standards/` returns nothing; `grep -n 'OptionsCompose' standards/standards/library-stack.md` resolves. | — | S |
| **M1-STD-16** | WowAddonStandards | Version rollup: `STANDARDS.md:1` version and date, changelog entry naming every section touched by `M1-STD-01` … `-15`, Sections map, anti-pattern range. Ripple into the context pack and the three playbooks wherever a process line changed. **Last in Group B.** | `head -1 standards/STANDARDS.md` shows the new version; no document outside an amended section still restates the old text. | M1-STD-01 … M1-STD-15 | M |

**Safely parallel inside Group B:** every item except `M1-STD-16`, which is last, and `M1-STD-01` and
`M1-STD-13`, which each follow a Group A item.

## M1 · Group C — the `wow-addon` plugin

Path: `/mnt/d/Profile/Users/Tushar/Documents/GIT/wow-addon`. All six are docs-only and mutually
independent.

| ID | Repo | What changes | Verified by | Depends on | Effort |
|---|---|---|---|---|---|
| **M1-WA-01** | wow-addon | `agents/review.md`: add a cross-addon, same-session pass. The whole checklist is per-addon today and its only cross-repo line is `## Interface:` consistency, while the collection's stated deployment is all nine loaded together. Name the four collision classes: slash tokens, vendored LibStub minors, byte-divergent vendored files, `## Interface`. | `grep -n 'same session\|cross-addon' agents/review.md` resolves. The pass, run today, reproduces the clean result recorded in `01_CONSOLIDATED_FINDINGS.md`. | — | M |
| **M1-WA-02** | wow-addon | `agents/review.md` and `agents/standards-audit.md`: every census command counts the whole tracked set and states its scope. Four of this cycle's counts were wrong, in both directions and at both stages — `C22`'s eleven against a measured 18, `C08`'s "46 of 89" against 35 of 93, `CX08`'s 75 "corrected" to a PrettyChat 93 that counts a generated tree this plan exempts by rule, and a `246`/`138` chrome pair measured over `libs/` when every other sweep excludes it. Each came from a scope nobody wrote down, and the `CX08` pair is the sharpest case because **the correction was wrong and the original was right**: a second pass with no stated scope is not a check, it is a second guess. | `grep -n 'git ls-files' agents/review.md` resolves inside the census guidance. | M1-STD-08 (so the cap's scope matches what is counted) | S |
| **M1-WA-03** | wow-addon | `commands/revendor-libka0s.md`: check for a **contract** change, not only a version change. `M1-LK-02` moves `__AttachCompose` from tolerating a table-returner to requiring a function, and MultiMeters ships the tolerated shape — a version-only delta report would not have seen it. | `grep -n 'contract' commands/revendor-libka0s.md` resolves in the delta section. | — | S |
| **M1-WA-04** | wow-addon | `commands/sync-docs.md`: add a comment-citation check over the addon's own source (excluding `libs/`, `tests/_kit/`) — extract path-like tokens and `Symbol.Member` references from comments, report those that do not resolve, apply comment-only on confirmation. This is `C19`'s standing gate: roughly forty rotted citations across seven repos. | `grep -n 'comment-citation' commands/sync-docs.md` resolves. Running it against `LootHistory/core/Database.lua:195` reports the "v6->v9" citation. | — | M |
| **M1-WA-05** | wow-addon | `commands/new-addon.md`: scaffold a non-English-client step into `docs/smoke-tests.md`. Six of nine addons have none, including the two whose code is most locale-sensitive — LootHistory, whose `core/Compat.lua:188-195` defines four English wordings as the fallback when the client leaves `ITEM_ACCOUNTBOUND*` nil, and PrettyChat, whose entire function is overwriting localized `_G` chat format strings. | `grep -n 'locale' commands/new-addon.md` resolves in the smoke-test section. | — | S |
| **M1-WA-06** | wow-addon | Put WowAddonStandards and `wow-addon` into the audit rotation. Neither has ever had a review or an audit; `agents/review.md` (321 lines) and `AUDIT.md` (515 lines) drove all twenty of this cycle's passes, so a defect in either was reproduced twenty times and reviewed zero. Both are docs-only, which is presumably why they were skipped. **`Ka0sAddonsCommonTasks` is the third unaudited repository and is deliberately not added**: it holds a `README.md` and a `docs/` tree of frozen planning bundles — no Lua, no TOC, no `libs/`, no suites — so `AUDIT.md`'s checklist has nothing to bind to, and auditing it would manufacture findings the same way `library-stack-§7` says auditing a library against the addon rule set does. Its bundles are evidence, governed by the frozen-bundle rule. | Both repos hold a `docs/audits/<date>/` bundle. Ka0sAddonsCommonTasks holds none, and `00_OVERVIEW.md` says why. | — | M |

### M1 exit criteria

- `git ls-files --eol` in LibKa0s reports no `w/lf` or `w/mixed` outside the two `eol=lf` scripts —
  **all seven** files `M1-LK-00` names, not only the two in the payload — and
  `diff -r LibKa0s <Addon>/libs/LibKa0s` is byte-empty for the first consumer re-vendored.
- `lua tests/run.lua` in LibKa0s is green, and the four `M1-LK-01` cases were **seen red** before
  `M1-LK-02` landed.
- Tags `v1.26.0` and `v1.27.0` each carry a release bundle naming them.
- `docs/api/` carries a document for every minor moved: Options 15, Compose 3, Widgets 14, Kit 15.
  `tests/test_versioning.lua` cannot go green otherwise, so this is enforced rather than remembered.
- The standard's version, date, changelog, Sections map and anti-pattern range are rolled, and no
  document outside an amended section still restates the old text.

---

# M2 — the defects that need no upstream anything

**Starts on day one, in parallel with M1.** Nothing here waits on a tag, a section amendment or a
re-vendor. Six lanes, each in a different repository, so an operator and an AI pair can interleave them
freely — with one rule: **the serialisation point inside any repo is `settings/OptionsSetup.lua`**, and
never two agents in that file at once.

## M2 · Lane A — PrettyChat

| ID | Repo | What changes | Verified by | Depends on | Effort |
|---|---|---|---|---|---|
| **M2-01** | PrettyChat | Move `conversionSequence` into `modules/Override.lua` as `NS.ConversionSequence`; `Schema.Set` (`settings/Schema.lua:464`) refuses a write whose sequence is not a positional prefix of the shipped default's. Today `row.set` stores any string and `buildSampleArgs` (`modules/Override.lua:275-292`) synthesises arguments from the format itself, so the Preview can never see a surplus conversion — the raise happens later, inside Blizzard's chat handler. | A case sets a format with a surplus `%s` and asserts refusal; another asserts a valid one is stored. `tests/test_defaults.lua` asserts the prefix rule, not equality. | — | M |
| **M2-02** ⚠ | PrettyChat | Replace `settings/Panel.lua:646-721`'s hand-copied landing renderer with `H.BuildLandingPage(ctx, spec)`, and publish a `BuildLandingPage` no-op in `settings/OptionsSetup.lua`'s stub. The library's renderer sets, at `OptionsWidgets.lua:323`, the `OnRelease` that hides the logo; the copy sets none, so a 300px texture rides AceGUI's pooled `SimpleGroup` into the next widget — **and that pool is shared with every other addon in the session**. | `grep -n 'buildParentBody' settings/Panel.lua` returns nothing. **Smoke, session 3:** open PrettyChat's landing page, page to another addon's settings, confirm no logo rides through. | — | M |
| **M2-03** | PrettyChat | `core/PrettyChat.lua:20-25` builds a fresh merged table instead of mutating `NS.ProfileDefaults` in place; `modules/Override.lua:154` tracks global presence in a separate key set so a global this client does not define is restored to nil on disable rather than skipped. Publish a nil-returning `MakeCloseButton` in the degraded branch (`core/CoreSetup.lua:74-85`) and add it to `coreSurface`. | Cases for each, red under today's code. `grep -n 'ProfileDefaults' core/PrettyChat.lua` shows no in-place write. | — | S |

## M2 · Lane B — BankLedger and ConsumableMaster (SavedVariables)

**The highest blast radius in the plan.** A wrong fix here corrupts a real ledger, and both defects are
pinned by tests that cannot go red — so in both cases **the fake is fixed before the code**.

| ID | Repo | What changes | Verified by | Depends on | Effort |
|---|---|---|---|---|---|
| **M2-04** | BankLedger | `tests/wow_mock.lua:582-589` models AceDB's default fallback — metatable or logout strip — so that setting a key nil is observably different from the default being present. Today it returns `deepcopy(defaults.global)` and the kit fake copies defaults in too, so the boundary case at `tests/test_database.lua:330` cannot fail. **No assertion is weakened.** | The absent-`schemaVersion` case turns red against today's `defaults/Global.lua`. That red is the deliverable. | — | M |
| **M2-05** ⚠ | BankLedger | Drop `schemaVersion` from `defaults/Global.lua:14`; `RunMigrations` (`core/Database.lua:15-21`) seeds it, using an empty ledger to separate a fresh install from a pre-stamp store. Today `g.schemaVersion or 1` always reads the current version and the `< NS.SCHEMA_VERSION` arm at `:21` never runs. | `M2-04`'s case goes green. **Smoke, session 2:** back up SavedVariables, hand-edit a **copy** to drop `schemaVersion` and add a `vendorPrice` row, log in, expect `v1 -> v2, 1 rows touched`, log out, confirm the stamp persisted. | M2-04 | M |
| **M2-06** | ConsumableMaster | `tests/test_database.lua:56-63` is renamed to what it asserts and gains the missing multi-profile case; its second assertion, which pins the account-wide key the defect is, is revisited alongside `M2-07`. | The multi-profile case is red against today's `core/Database.lua`. | — | S |
| **M2-07** ⚠ | ConsumableMaster | `core/Database.lua:65-90`: gate profile-writing steps on `db.profile.schemaVersion`, keep account-wide steps on `db.global`. Today both steps write `db.profile` while the stamp is account-wide, so the `OnProfileChanged` hook at `core/ConsumableMaster.lua:401-410` is inert on a second profile. | `M2-06`'s case goes green. **Smoke, session 2:** create and switch to a second profile, confirm the migration line fires. It does not today. | M2-06 | M |
| **M2-08** ⚠ | ConsumableMaster | `settings/Panel.lua:866-867`: defer `Settings.RegisterAddOnCategory` on `InCombatLockdown` and retry from the existing `PLAYER_REGEN_ENABLED` handler. The bootstrap at `:984-993` fires it from `PLAYER_LOGIN`/`ADDON_LOADED` with no guard, which an in-combat reload reaches. | **Smoke, session 1:** `/reload` while in combat, confirm no taint error and that the category registers on leaving combat. | — | S |

## M2 · Lane C — MultiMeters (the feign-trace subsystem)

| ID | Repo | What changes | Verified by | Depends on | Effort |
|---|---|---|---|---|---|
| **M2-09** | MultiMeters | Publish a plain boolean (`Diagnostics.feignArmed`) and read it before building anything: hoist the read above the per-source loop at `modules/Aggregator.lua:1488-1496`, and check it before the fields table and its nested order table at `modules/Feign.lua:102-105` and `:274-281`. Today a disarmed trace allocates two tables per Deaths source per refresh. `Diagnostics.IsFeignTraceArmed` (`core/Diagnostics.lua:1618`), which has no production caller, reads the same field. | A perf scenario measures a Deaths refresh with the trace disarmed and asserts zero attributable allocation. Written **first**, red. **Plus a `lizard` delta**: `modules/Aggregator.lua:1488-1496` is inside `scanColumn@1439-1540`, **CCN 36 — the highest function in the collection** — and this repo's 23 warnings already block its release gate, so the item records `scanColumn`'s CCN before and after and does not raise it. | — | M |
| **M2-10** | MultiMeters | Stop `judge` evicting the cast lines the ring exists to show: admit it only for GUIDs a cast line named, with a suppressed-row counter, or give each kind its own bounded ring. `FEIGN_TRACE_MAX = 120` at `core/Diagnostics.lua:1604`; replace `:1643`'s `table.remove(log, 1)` with a write index into a fixed table. | A case asserts a cast line survives a full ring of `judge` rows. Red today. | M2-09 | M |
| **M2-11** ⚠ | MultiMeters | Trace the eviction branch at `modules/Feign.lua:247-249` with its own verdict — today `if unit == nil then feigned[guid] = nil` falls through silently, and it is the path most likely to explain issue #25. Hoist the prior state above the eviction at `:280` so `noted` and `down` stay distinguishable. `settings/Slash.lua:470-484` names a rejected argument and returns instead of falling through to `ReportFeign` — `/mm debug of` currently prints a report and leaves the trace armed. | Cases for all three. **`lizard` delta recorded**: `modules/Feign.lua:247-249`/`:280` sit inside `Feign.Prune@227-285` (CCN 26) and `settings/Slash.lua:470-484` inside `doDebug@434-494` (CCN 23); a new verdict arm and a new rejection arm each add a branch to a function already over the gate, so both figures are stated before and after. **Smoke, session 1:** `/mm debug of` prints a rejection line and leaves the trace disarmed — today it prints the full report and leaves it armed. | M2-09 | S |
| **M2-12** | MultiMeters | Re-derive `tests/perf.lua:564`'s `PROBE_OFF_BYTES_CEILING` from three runs after `M2-09`, recording the measured figure, the margin and the date. It reads 336000 against a commented 325955 and a measured 310158.1, so the stated 3.5% headroom is 7.7%. Then re-run and close or re-triage GitHub issue #17, whose ceiling-breach claim no longer reproduces. | `lua tests/perf.lua` exits 0 with the new ceiling; the comment names the run. | M2-09 | S |

## M2 · Lane D — LootHistory

| ID | Repo | What changes | Verified by | Depends on | Effort |
|---|---|---|---|---|---|
| **M2-13** | LootHistory | `core/Database.lua:748-754`: sum the seven string fields inline instead of walking a literal array with `ipairs`, which runs zero iterations for a currency record built without an `itemLink` (`modules/Collector.lua:190-196`) and charges flat overhead. The per-record allocation disappears with the same two lines. | `tests/test_database.lua:379` asserts an exact byte total over a fully populated fixture plus a currency row, with a `-- red under:` comment. It passes today at 512 bytes of pure overhead, which is the defect. | — | S |
| **M2-14** | LootHistory | `settings/Panel.lua:155-162`: wrap the `RecordAdded` handler in `NS.Coalesce(onChange, NS.Constants.RECORD_ADDED_COALESCE)`, as `modules/Browser.lua:1273` and `modules/Analytics.lua:655` already do. `HistoryChanged` stays immediate. | A case asserts N record-added events produce one `StorageStats` pass. | — | S |
| **M2-15** | LootHistory | Add an integration case calling `modules/Attribution.lua:327-361`'s `Enable()` against the mock, asserting the registered event set and the hooked globals. It has zero test callers today, so seven events, one unit frame and five hooks are entirely uncovered. Publish `tests/run.lua:43-47`'s lifecycle kick through `Kit.expose` and pin it against `OnInitialize`'s actual call set, which it misses by one (`NS.Slash:Register`). | Deleting one `RegisterEvent` from `Enable()` turns the case red. Adding a call to `OnInitialize` without the runner turns the pin red. | — | M |

## M2 · Lane E — the `SetRenderer` adoption (AbsorbTracker, KickCD, MultiMeters)

`O.SetRenderer` is published at `LibKa0s/Options.lua:695` with the Blizzard-sidebar combat refusal inline
at `:700-716`, and vendored in all nine repos today. This lane is adoption, not a library dependency.

| ID | Repo | What changes | Verified by | Depends on | Effort |
|---|---|---|---|---|---|
| **M2-16** ⚠ | AbsorbTracker | Move `settings/Appearance.lua:320`, `General.lua:283` and `Profiles.lua:57` onto `Helpers.SetRenderer`, drop their own `EnsureDefaultsButton` calls, and **publish `SetRenderer` in `settings/OptionsSetup.lua`'s stub in the same commit** — the stub omits the member entirely today, which is why nothing went red. AbsorbTracker is the only repo in the collection with zero callers, and its own `docs/settings-panel.md:278-285` documents the refusal it does not deliver. | `grep -rn 'SetScript("OnShow"' settings/` returns nothing that renders a page. **Smoke, session 1:** in combat, open AbsorbTracker from the Blizzard AddOns sidebar and expect the refusal plus a closed panel. | — | M |
| **M2-17** ⚠ | KickCD | Same, for the Profiles and Spells pages. | As above, `/kcd`. **Smoke, session 1.** | — | S |
| **M2-18** ⚠ | MultiMeters | Same, for the Profiles page. | As above, `/mm`. **Smoke, session 1.** | — | S |

## M2 · Lane F — packaging, taint and the remaining event gaps

| ID | Repo | What changes | Verified by | Depends on | Effort |
|---|---|---|---|---|---|
| **M2-19** | AbsorbTracker, WhatGroup, LootHistory, KickCD, PanelMaster, PrettyChat, ConsumableMaster | The `.pkgmeta` omissions that need no template change. **Two kinds, and only the first is player bytes.** (a) **Tracked and shipped:** `media/screenshots` is tracked in every repo and ignored in only three, so four addons ship it — **KickCD 7.5M, LootHistory 5.9M, AbsorbTracker 2.0M, WhatGroup 880K, 16.3M in total** — plus WhatGroup's `CLAUDE.md` and `DEPENDENCIES.md`, keeping `README.md` and `LICENSE`. (b) **Present at the root, untracked, and therefore not in any packager clone** — `.claude` and `.superpowers` in AbsorbTracker, KickCD, PrettyChat and ConsumableMaster, `.superpowers` and `.pytest_cache` in LootHistory. Zero player bytes, and listed because `packaging.md:28`'s strong form MUSTs that every root dotfile and dot-directory **present in the repo** either appear in the ignore list or be justified beside it, tracked or not. Also `.gitattributes` in LootHistory and PanelMaster, `_dev` in ConsumableMaster. Each entry carries a one-line comment, and the (b) entries say *untracked; listed under `packaging.md:28`* so the next reader does not re-file them as shipping. | `git ls-files` in each repo, filtered through that repo's `.pkgmeta` ignore list, returns no `media/screenshots/`, no `CLAUDE.md`, no `DEPENDENCIES.md`. There is no packager dry-run to run: no repo carries `.github/workflows` and `packaging.md:32` puts CI out of scope, so a zip listing was never an available check. | — (the `.pkgmeta` template line is `M1-STD-09`, and does not block these) | S |
| **M2-20** ⚠ | WhatGroup | Delete `settings/Schema.lua:577`'s `StaticPopupDialogs = StaticPopupDialogs or {}`, keeping the indexed write below it. The table always exists in retail, so the guard is dead code — and it sits directly under a comment explaining that registration is deferred precisely to avoid touching the table. | **Smoke, session 1:** invoke the reset popup in combat and out, confirm no "Interface action failed because of an AddOn". A taint bug never surfaces as a test failure. | — | S |
| **M2-21** ⚠ | WhatGroup | `modules/Frame.lua:148-151`: register `PLAYER_REGEN_DISABLED`/`ENABLED` and route both to `ApplyFrameVisibility`, made symmetric — hide when the gate closes, show when it opens with `pendingInfo`. The gate is evaluated at every `ShowFrame` (`:665`) today, so the option is not inert; only the mid-window transition is missed. Also `:275`: arm the cooldown ticker only when the frame is shown, and amend the register row whose "cannot outlive that window" claim is currently false. | A case entering and leaving combat asserts the frame follows. **Smoke, session 1:** enter combat with the frame shown, confirm it hides; leave with a pending invite, confirm it returns. | — | M |
| **M2-22** ⚠ | WhatGroup, BankLedger, KickCD | Three unrelated event gaps. WhatGroup `core/WhatGroup.lua:678`: key captures by `searchResultID` through the existing `GetApplicationInfo` bridge instead of binding `table.remove(captureQueue, 1)` to whatever application id arrives, and clear `pendingApplications` on declined and cancelled; `:605`: move the `autoShow` read inside the scheduled callback, which already re-reads `pendingInfo` for exactly this reason. BankLedger `settings/Slash.lua:92-103`: send `Ka0s_BankLedger_SettingsChanged` once at the end of `ResetEverything`, so `modules/Ledger.lua:872-878`'s capture gate re-caches instead of staying stale until reload. KickCD `modules/Castbar_Debug.lua:42`: print the secret branch unconditionally with `C_CurveUtil` availability as a separate clause. | A case per repo, each red today. WhatGroup's is two outstanding applications pairing correctly. **Smoke, session 1:** apply to two group-finder listings and let both resolve, one accepted and one declined, confirming each notification names its own group; `/bl` reset everything then capture a bank movement without reloading; `/kcd` debug dump with and without `C_CurveUtil`. | — | M |

| **M2-23** | all nine addons, LibKa0s, WowAddonStandards | **Reconcile the live issue store against this bundle, before M2 closes.** `gh issue list` returns **91 open issues** today — AbsorbTracker 11, BankLedger 3, ConsumableMaster 11, KickCD 9, LootHistory 4, MultiMeters 13, PanelMaster 20, PrettyChat 6, WhatGroup 3, LibKa0s 10, WowAddonStandards 1 — and this bundle names six of them in passing. The collection's tracking lives in GitHub issues, so a 207-finding plan that exists only as markdown in a thirteenth repository is invisible to `/wow-addon:issue-details` and to every future triage. Per issue, one of three dispositions: **covered** (name the cluster and the work item), **unaffected** (say why), or **contradicted** (this plan decides differently — say so on the issue and re-triage it). Start with the seven live `severity:high` rows the plan opens repositories for and does not mention: MultiMeters #22, #24, #25, #26, KickCD #7, #8, LibKa0s #15 — **#15 is this collection's Critical, already filed and still `state:untriaged`**, and `M3-04` closes it. | Every open issue in the eleven stores carries one of the three dispositions, recorded as an issue comment. `gh issue list --label state:untriaged` in LibKa0s no longer returns #15 unremarked. Throttle the writes — space the comment calls out rather than firing 91 at once. | — | M |

## M2 · Lane G — the previously unmapped findings

**Added 2026-09-07 by the owner's decision on `00_OVERVIEW.md`'s decision 4: do all seven.** These are
the rows `05_TRACEABILITY.md` § Part 3 held as the plan's own coverage defect — four specified in
`03_SPEC.md` and scheduled nowhere, three in neither document. Four of them are one-line edits in files
this milestone already opens, which is exactly why they were easy to lose. Two need something other than
a commit and are at `M5-09` and `M5-10` rather than here. **With this lane the plan maps 207 of 207
findings and § Part 3's unmapped set is empty.**

**Safely parallel across all four** — three repositories, no shared file.

| Item | Repo | Change | Verification | Deps | Effort |
|---|---|---|---|---|---|
| **M2-24** | LootHistory | `settings/Slash.lua:178-181`: add `config` to the set subtracted from the help list on a library-less load, and carry the `LIBRARY_OWNED` rename the finding names so the set says what it is. Today `/lh help` advertises a verb that cannot run in that configuration. | A case builds the help list with the library absent and asserts `config` is not in it. Red today. | — | S |
| **M2-25** | WhatGroup | Two one-line edits in `settings/Panel.lua`, one commit. `:285` keys off `Helpers.MASTER_GROUP` instead of the `"Master controls"` string literal — `O.MASTER_GROUP` is published at `OptionsCompose.lua:189` **in the payload WhatGroup vendors today**, so this needs no re-vendor and is not M4 work. `:207` passes the `addonName` upvalue the file already binds at `:14` instead of re-deriving it. | `grep -n '"Master controls"' settings/Panel.lua` returns nothing. A case pins the upvalue at `:207`. Satisfies two of `03_SPEC.md` § `C30`'s five acceptance criteria. | — | S |
| **M2-26** | BankLedger | Add `addon:OnDisable` to `core/BankLedger.lua:44-59`, clearing `_enabled` on Ledger, Browser, SessionWindow and Insights. `modules/Ledger.lua:845-847`'s `Enable` early-returns on `_enabled` and nothing in the repo calls `Disable`, so a disable-enable cycle leaves every module inert. **`_guildHooked` is verified separately** — it is not part of the `_enabled` cycle and clearing it here would unhook a live hook. | A case disables then re-enables the addon and asserts all four modules are live again. Red today. `03_SPEC.md` § `C29` names five items for seven findings; this is one of the two it dropped. | — | S |
| **M2-27** | BankLedger | `settings/Schema.lua:438-442`: distinguish unavailable from off. With `NS.LedgerTable` absent, `on` is nil and `/bl test` prints "test mode off", which is a lie about a module that is not there. Use the shape the session verb two rows up already uses for exactly this case. | A case with `NS.LedgerTable` nil asserts the unavailable wording, not "off". | — | S |

---

# M3 — adoption of v1.26.0

**Ordered, and the order is not alphabetical.** Because `OptionsCompose.lua:32-35` resolves the highest
compose minor present in the session, `M3-01` alone repairs the composed dropdowns for every consumer in
a live client — so the wave does **not** have to be atomic, and step one can be seen working before step
two opens. Steps 2–5 are still required: a session carrying only stale copies is back to the defect.

| ID | Repo | What changes | Verified by | Depends on | Effort |
|---|---|---|---|---|---|
| **M3-01** ⚠ | KickCD | Re-vendor `libs/LibKa0s/` and `tests/_kit/` whole from v1.26.0, rolling the `CLAUDE.md` provenance line in the same commit — **and, in that same commit, rewrite `Helpers.LSMValues` (`settings/Panel.lua:346`) to return the deferred closure instead of the hash.** Non-optional, for the same reason `M3-02` gives for MultiMeters: `NS.Settings.Helpers` **is** the library instance, decorated in place, so `function Helpers.LSMValues` **is** a shadow of `O.LSMValues` — written as a decoration, not as an `O.LSMValues =` assignment, which is why the survey that caught MultiMeters missed it. The eight composed sites (`settings/Castbar.lua:346`, `:481`, `:503`, `:514`, `:536`, `settings/Icons.lua:207`, `:258`, `settings/Label.lua:184`) sit inside per-unit loops over `NS.Units.LIST = { "target", "focus" }` and emit **16** media rows. They **keep** working — they were never broken; see the note below. | `diff -r --strip-trailing-cr ../LibKa0s libs/LibKa0s` empty **and** `diff -r ../LibKa0s libs/LibKa0s` byte-empty. `lua tests/run.lua` green **at 841**, unchanged either side. The three cases that go red on the re-vendor alone are the gate: `test_color_shape`'s "an LSM-backed row resolves its values at call time" and "every static dropdown declares its order", and `test_schema`'s default-in-values check. **Smoke, session 4:** `/kcd config` → Icons, Label and Castbar dropdowns list real faces, borders and textures; `/dump LibStub("LibKa0s-Options-1.0").MODULES.OptionsCompose` reports 3. **This is the proof the re-vendor did not silently freeze the lists** — for KickCD it is a regression check, not proof of a repair. | M1-LK-04 | S |
| **M3-02** ⚠ | MultiMeters | Re-vendor **and** revert `settings/Schema.lua:670` to `C.LSMValues = lsmValues` **in the same commit**. Non-optional: `M1-LK-02` moves `__AttachCompose` from calling a host's `LSMValues` at render time to calling it once at row-declaration time, so MultiMeters' table-returner would hand the composer a table frozen at file load — no crash, no warning, and exactly the failure `Options.lua:759-763` says the deferral prevents. | `grep -n 'C.LSMValues' settings/Schema.lua` returns exactly `C.LSMValues = lsmValues`. **Smoke, session 4:** open a MultiMeters media dropdown after a media addon has registered a face, confirm the face is listed. | M3-01 | S |
| **M3-03** | AbsorbTracker | Re-vendor, then delete `LSM_KIND` and `fixMediaValues` (`settings/Appearance.lua:114-137`) and its three call sites at `:181`, `:237`, `:257`. The comment at `:121-129` says "delete this the re-vendor after the fix lands". | `grep -rn 'fixMediaValues\|LSM_KIND' settings/` returns nothing; `lua tests/run.lua` green with `tests/test_schema.lua`'s pin updated in the same commit. | M3-01 | S |
| **M3-04** | ConsumableMaster | Re-vendor, then delete `lsmValues` (`settings/MacroBar.lua:121-123`) and the three row overrides at `:269`, `:337`, `:454`. Close LibKa0s issue #15, which the comment at `:118` names. | `grep -n 'lsmValues' settings/MacroBar.lua` returns nothing; `gh issue view 15 -R <LibKa0s>` shows closed. | M3-01 | S |
| **M3-05** | BankLedger, LootHistory, PanelMaster, PrettyChat, WhatGroup | Re-vendor only. These five consume `MasterControls` and `ColorPair` and no media composer, so nothing moves. **Safely parallel across all five.** | Both diffs empty in each; `lua tests/run.lua` green in each; pass counts unchanged. | M1-LK-04 | S |

> **Correction (`M4-C2`), against shipped `e3274f6`.** This row read "**No KickCD code change.** Eight
> composed rows start working". Both halves were wrong, and in opposite directions.
>
> KickCD never had `LIBKA0S-A-01`. Its shadow returned the **hash**, so against the old double wrap the
> composer's own `function() return O.LSMValues(m) end` deferred the read and the dropdowns filled.
> Measured at `e3274f6^` (v1.25.0): **841 passed, 0 failed**, and all **16** media rows carry
> `values = function`. Nothing was waiting to start working.
>
> What the re-vendor does to KickCD is the reverse. `COMPOSE_MINOR` 3 drops the wrapper and assigns
> `values = O.LSMValues("font")` **once, at row-declaration time**, so the shadow's hash is read while
> `settings/Icons.lua` is still being parsed. Measured, v1.26.0 against the unchanged
> `settings/Panel.lua`: all 16 rows become `values = table`, frozen before any media addon has run, and
> **3 cases go red**. In game that is silent — no error, no empty control, a list that never grows.
>
> So the 43 lines in `settings/Panel.lua` are the fix that keeps the re-vendor green, not scope the item
> took on. The plan's mistake was a survey shape: it grepped for hosts assigning `O.LSMValues` and found
> MultiMeters' `settings/Schema.lua:670`, but KickCD writes its shadow as `function Helpers.LSMValues`
> on the instance it decorates in place, so the grep never saw it. `M3-02`'s "non-optional" applies to
> KickCD word for word; the plan applied it to one addon and should have applied it to two.

---

# M4 — adoption of v1.27.0, and the compliance the rulings unblock

One re-vendor wave carrying both payloads, then the work each upstream item unblocks. **The
serialisation point inside every addon is `settings/OptionsSetup.lua`**: `M4-02`'s patch call site,
`M4-09`'s parity case and — where they landed in M2 — `CX03`'s stub line and `C07`'s no-op all live in
that one file.

| ID | Repo | What changes | Verified by | Depends on | Effort |
|---|---|---|---|---|---|
| **M4-01** ⚠ | all nine | Re-vendor `libs/LibKa0s/` and `tests/_kit/` whole from v1.27.0, rolling each `CLAUDE.md` provenance line in the same commit. Kit and payload move together because `docs/releasing.md:131-137` copies both and each repo's `tests/test_vendor_sync.lua` gates both against the one tag the provenance line names. | Both diffs empty in each of the nine. `grep -h 'Kit.VERSION' */tests/_kit/framework.lua \| sort -u` → one line, 15. Pass counts unchanged — `M1-LK-08` is additive by design. **Smoke, session 3:** `M1-LK-03` rewrites `TabStrip` to acquire its buttons and content panel from a pool and re-set `OnClick` per dress, and `TabStrip` renders in the live settings code of **all nine** addons; its only headless proof counts `CreateFrame`, and the four `C12` findings that would pin band geometry under selection are deliberately deferred to kit 16. So open every multi-tab settings panel in each of the nine, cycle its tabs three times, and confirm labels, selection state and band height are unchanged. | M1-LK-15, M3 | M |
| **M4-02** | AbsorbTracker, ConsumableMaster, KickCD, MultiMeters, PanelMaster | Call `lib.__PatchLSM30Border()` from the live arm of `settings/OptionsSetup.lua`. **Leave all five `core/LSMPatch.lua` files in place.** | `lua tests/run.lua` green in all five. | M4-01 | S |
| **M4-03** ⚠ | — | **Smoke, session 5.** Load KickCD, PanelMaster, AbsorbTracker, ConsumableMaster and MultiMeters together and open each addon's Border dropdown in turn, in every load order that is convenient. The failure mode is "whichever addon loaded last owns everyone's dropdown", and no headless suite can see it. | Every Border dropdown draws the same styled control, and the styling does not depend on load order. | M4-02 | M |
| **M4-04** … **M4-08** | KickCD, PanelMaster, ConsumableMaster, MultiMeters, AbsorbTracker | Delete `core/LSMPatch.lua`, **one repository per commit, in that order**, re-running the session-5 smoke **after every one of the five deletions**. AbsorbTracker is last because it is the one real divergence: it exposes a callable `NS.ApplyLSMBorderPatch()` at `core/LSMPatch.lua:20` invoked from `core/AbsorbTracker.lua:52` rather than a `PLAYER_LOGIN` frame. KickCD and PanelMaster are functionally identical; ConsumableMaster differs in a bootstrap header line and MultiMeters in a `local _ = ...`. | `ls */core/LSMPatch.lua` returns nothing. `grep -rn 'RegisterWidgetType' <repo>/core <repo>/modules <repo>/settings | grep 'LSM30'` returns nothing in any repo. A bare `RegisterWidgetType` hit is EXPECTED wherever an addon owns the type name it registers; what must be gone is a registration against the shared `LSM30_*` slots (**corrected by `M4c-03`; see the note below**). Five commits means five bisect points if the sentinel is wrong. | M4-03 | M |
| **M4-09** | all nine | Add `tests/test_surface_parity.lua` calling `Kit.assertSurfaceParity(stub, majorName)` where one is missing — six of the nine have nothing today. AbsorbTracker's, ConsumableMaster's and KickCD's are rewritten onto the factory. | Deleting one member from a repo's stub turns its case red. AbsorbTracker's is red without `SetRenderer`, which `M2-16` added. | M4-01, M2-16 | M |
| **M4-10** | all ten | The line-ending working-tree sweep, now that the gate exists and is vendored. **`git add --renormalize .` is the wrong tool and produces no repair**: the index is already LF everywhere, so it rewrites nothing and leaves the working tree exactly as it was — which is why nothing has ever reported these. The repair is `rm <path> && git checkout -- <path>` per file, which is what `tests/test_eol.lua`'s own failure message tells you to run and what `M1-LK-00` does in the library. **Re-enumerate before sizing** — measured today over `git ls-files --eol \| grep -E 'w/(lf\|mixed)'` minus the `attr eol=lf` scripts: MultiMeters 21, LootHistory 9, KickCD 8, ConsumableMaster 7, LibKa0s 7 (cleared early by `M1-LK-00`), PanelMaster 6, WhatGroup 6, BankLedger 4, PrettyChat 4 — four, not the two `PRETTYCHAT-A-07` recorded, because that finding scoped itself outside `libs/` and the other two are `libs/LibKa0s/DebugLog.lua` and `Pool.lua` inside the **shipped** payload — AbsorbTracker 2. State per repo which frozen-bundle paths were excluded. | `git ls-files --eol \| grep -E 'w/(lf\|mixed)'` returns only files under `attr eol=lf` in each of the ten. The vendored EOL suite is green. | M4-01 (the gate arrives with the kit) | M |
| **M4-11** | all nine | Narrow `.luacheckrc`'s `exclude_files` to `tests/_kit/` and add the `files["tests/"]` stanza, following the shape `M1-LK-12` proved. Fix what the newly-linted 308 test files report. **Never a blanket ignore** — an ignore that silences the wall reads as coverage and provides none, which is worse than the exclusion. WhatGroup additionally adds `_dev/`, so its `.luacheckrc:9` and `.pkgmeta:12` agree. | `luacheck .` 0/0 in each of the nine with the test tree in scope. | M1-STD-01 | M |
| **M4-12** | KickCD, PrettyChat, WhatGroup | The eight load-bearing TOC annotations `M1-STD-02`'s denominator leaves standing: `KickCD.toc:55`, `:73`; `PrettyChat.toc:40`, `:57`; `WhatGroup.toc:44`, `:47`, `:53-56`. One at-line comment each naming the symbol and its publisher, in the shape `AbsorbTracker.toc:39-40` already uses. | A fresh `/wow-addon:standards-audit` files no per-line `toc-file-§5` MUST row against any of the nine TOCs. | M1-STD-02 | S |
| **M4-13** | ConsumableMaster, KickCD, WhatGroup | The spelling sweeps, against the list `M1-STD-12` publishes. ConsumableMaster 25 live sites (the audit's 28 folded in two vendored files); KickCD 37 hits across 11 live files (the audit's 51 folded in frozen bundles); WhatGroup three comments at `modules/Frame.lua:267`, `settings/Schema.lua:115`, `settings/OptionsSetup.lua:92`. Live files only — no `libs/`, no frozen bundle. Regenerate `docs/test-cases.md` where a case name moves. | `grep -rniE 'colour\|behaviour\|grey' <repo> --exclude-dir=libs --exclude-dir=_kit --exclude-dir=audits --exclude-dir=reviews --exclude-dir=automated-tests` returns nothing. | M1-STD-12, M1-LK-11 | M |
| **M4-14** | MultiMeters, ConsumableMaster, PanelMaster, LibKa0s, PrettyChat | Disposition every file still over the 1500-line cap after `M1-STD-08`'s ruling: an open issue naming the seam, or a register row with a re-check trigger. **No splits in this plan.** PanelMaster's `settings/PanelEditor.lua` (1350) is the one file whose own recorded trigger has fired — "if the next change also grows it, execute the split rather than re-accept" — so it needs a decision either way. PrettyChat's `GlobalStrings/GlobalStrings.lua` (23,842) is exempt by rule, being generated, unloaded and `.pkgmeta`-ignored. | No file sits over the cap unremarked in any repo. | M1-STD-08 | M |
| **M4-15** ⚠ | PanelMaster | Move the five Panels-page acts — Copy `:607`, Enabled `:633`, Unlock `:648`, Reset `:667`, Delete `:673`, all inside `sections[TAB_GENERAL]` — into the `H.PageHeader` band drawn at `settings/PanelEditor.lua:1112-1199`; drop the emptied General tab; re-point the `:1058` fallback; rewrite `docs/settings-panel.md:257`'s paragraph arguing the current placement, in the same commit. | A case asserts the five acts are in the band. **Smoke, session 3:** `/pm` → Panels, confirm the five controls are in the chrome band and each still works. | M4-01 | M |
| **M4-16** ⚠ | AbsorbTracker, KickCD, MultiMeters | Delete the perf-panel `decorate` field — `core/PerfSetup.lua:149-159` in AbsorbTracker, `:217-226` in KickCD, and MultiMeters' equivalent. `LibKa0s/PerfPanel.lua:191-196` draws the identical control anchor for anchor and the descriptor already supplies what it needs (`addonName` at AbsorbTracker's `PerfSetup.lua:43`, `name = addonName` at KickCD's `:69`). | A case asserts the descriptor carries `addonName` and no `decorate`. **Smoke, session 3:** `/at perf`, `/kcd perf`, `/mm perf` each open with one close button in the same place. | M4-01 | S |
| **M4-17** | AbsorbTracker, ConsumableMaster, KickCD, LootHistory, WhatGroup | Naming and config hygiene. Delete `AbsorbTracker/libs/LibStub/tests/` and `LibStub.toc`, leaving exactly what `AbsorbTracker.toc:17` loads. Prefix KickCD's six bare WoW globals with `_G.` (`modules/IconGrid.lua:232` beside `:148`, `modules/Cooldowns.lua:80`, `settings/Panel_Widgets.lua:121`, +3) and rename `modules/Castbar_Debug.lua`'s eight `print` parameters to `emit`, matching `settings/Slash.lua:61`. Change ConsumableMaster's three `%d` placeholders to `%s` (`settings/Category.lua:764`, `modules/Selector.lua:610`, `:655`) per `docs/debug.md:30`. Pin `LootHistory`'s `NS.version` (`core/Namespace.lua:5`) against `## Version:` with a TOC-parsing case. | `find libs/LibStub -type f` lists one file. Editing LootHistory's TOC version alone turns its suite red. | M4-01 | S |
| **M4-18** | AbsorbTracker, ConsumableMaster, KickCD, PanelMaster | Validate stored values at the boundary. Add `NS.GetThrottleWindow` beside AbsorbTracker's three clamped getters and call it from `modules/Timer.lua:50`; route `core/Units.lua:111-119`'s nineteen keys and the mirror flag through `NS.SetByPath`. Give ConsumableMaster one `colorDecode` returning nil for an absent channel, shared by `settings/OptionsSetup.lua:101-104` and `settings/Slash.lua:295-298`, which disagree today (`or 1` against `or 0`). Early-return in `KickCD/settings/Panel_Render.lua:304` rather than carrying a `y = -180` fallback against `defaults/Profile.lua:314`'s 120. In PanelMaster, treat `nums[4] <= 1` as already fractional under byte-scale RGB at `core/Util.lua:99-106`, and clear `NS.State.preview` in `modules/Registry.lua:588` through the same private sweep `dropSessionIDs` uses at `:561`. | A case per item, each red today. PanelMaster's round-trip colour cases cover the mixed-scale input. | M4-01 | M |
| **M4-19** | KickCD, LootHistory, MultiMeters, PanelMaster, WhatGroup, LibKa0s | Make the nine sleeping cases able to fail. Restore KickCD's shared instance in a guaranteed-run wrapper or take a fresh `T.load(true)` per case (`tests/test_schema.lua:581`, `:630`, `tests/test_options_panel.lua:552`) — `tests/_kit/framework.lua:613` pcalls the body, so a red skips the last-line restore. Assert MultiMeters' printed roster lines, not just `pcall` returning true (`tests/test_diagnostics.lua:1373-1381`). Call `NS.Version()` at `PanelMaster/core/Database.lua:141` and point the mock TOC version at a different string so `tests/test_database.lua:160` can fail. Pin WhatGroup's suite list in both directions (`tests/run.lua:59-77`), scan `media/` for any `.ttf`/`.otf` and any catalog filename (`tests/test_mediasetup.lua:147-155`), and assert `src ~= nil` before the `assertNil` at `tests/test_libka0s.lua:806`, deriving `SEAM_FILES` from the TOC-derived load list. | **Each case is seen red under the mutation its comment names, then green.** Dropping a suite from a runner's list turns that repo red. | M4-01 | M |
| **M4-20** | AbsorbTracker, ConsumableMaster, KickCD, PrettyChat | Dead code out, deliberate seams recorded. Delete `AbsorbTracker/settings/Schema.lua:101-111`'s `NS.PartitionUnitRows` with its only caller at `tests/test_schema.lua:524-530`, and reduce `core/Database.lua:95-112`'s `migrateAllProfiles` to `forEachProfile(NS.MigrateProfileToV3)`. Delete `KickCD/tests/test_bus.lua:48`'s pre-`KCD-09` branch and `modules/Castbar_Debug.lua:125`'s unreachable `or _G.print` arm with the spent note at `docs/ARCHITECTURE.md:278-284`. Delete `ConsumableMaster/tests/test_surface_parity.lua:169-174`'s duplicated paragraph and add `MakeCloseButton` to `CORE_SEAM` with a `CORE_LIVE_ONLY` entry. Record PrettyChat's three argued-in-place seams in `docs/module-map.md` rather than deleting them. | Case counts move by exactly the deletions, with `docs/test-cases.md` and the README badge in the same commit. | M4-01 | S |
| **M4-21** | ConsumableMaster, KickCD, LootHistory, PrettyChat | Route the remaining user-facing text through the `L` seam, and fix the coverage case that cannot see the gap. ConsumableMaster: take `local L = KCM.L` in `modules/KCMMacroDragIcon.lua` and `modules/KCMItemRow.lua` and wrap the six literals at `:74`, `:77`, `:171`, `:173`, `:175`, `:228`. KickCD: define the three current cast-bar desc sentences in `locales/enUS.lua` and drop the three superseded keys. LootHistory: match `[ \194\160]` rather than `%s` in the two localized-text trims (`core/Compat.lua:229`, `modules/Attribution.lua:66-67`). PrettyChat: wrap or record `settings/Slash.lua:241`, `:278-284`, `:349`, `:365`, `:379`, and correct `docs/ARCHITECTURE.md:228`'s claim that an unwrapped string is detectable. **Each repo's coverage case derives its candidate set from the TOC-derived source list rather than from a `gmatch` of `L["…"]`, which can only find strings already wrapped.** | Adding a bare literal to a settings file turns each repo's coverage case red. Every KickCD desc key used resolves in `locales/enUS.lua`. | M4-01 | M |
| **M4-22** | AbsorbTracker, ConsumableMaster, KickCD, LootHistory, PanelMaster | Re-baseline the ceilings that bound nothing and take only the measured allocations. `AbsorbTracker/tests/perf.lua:235`'s `PROBE_OFF_BYTES_CEILING = 320` cites 312.0 against a measured 48.0 — re-derive from three runs. Correct `PanelMaster/modules/Canvas.lua:654-656`, which claims the mouseover driver "stops doing any work the moment the tracked set is empty" and is false, and clear the script in `SetMouseoverTracked` when the set empties. `AbsorbTracker/modules/Display.lua:375` passes its open bucket as `Perf.Note`'s third argument, as `appearance:236` and `visibility:320` already do; give `settings/General.lua:218-229`'s throttle and console rows an explicit no-op `onChange` with a reason. **Take KickCD's per-cast closure (`modules/Castbar.lua:833`), LootHistory's provider map (`modules/AuctionPrice.lua:58,73`) and ConsumableMaster's per-call timer (`settings/Panel.lua:908-928`) only with a scenario that measures them, added first — otherwise skip them.** | Each ceiling carries its measured figure, margin and date. No allocation change lands without a scenario. | M4-01 | M |
| **M4-23** | LootHistory, MultiMeters | The two icon-catalog sites where the glyph exists: `LootHistory/settings/Panel.lua:459-461`'s READY, NOTREADY and INFO_ICON, and `MultiMeters/settings/ColumnBlocks.lua:60-61`'s `ENABLED_TEX`/`DISABLED_TEX`, whose comment cites ConsumableMaster parity — **so those two move together or neither moves**. Everything else stays. **The census, with its scope written down** — tracked `*.lua`, excluding `libs/`, `tests/` and `PrettyChat/GlobalStrings/` (generated, unloaded, `.pkgmeta`-ignored, and exempt by rule under `M1-STD-08`): **75 lines carrying 76 hard-coded `Interface\` paths**, which is the ledger's original figure — BankLedger 17, LootHistory 19, ConsumableMaster 11, MultiMeters 8, KickCD 7, PanelMaster 7, AbsorbTracker 3, WhatGroup 2, PrettyChat 1. Of those 76, **21 are `Interface\Buttons\WHITE8x8`** — the flat texture `standalone-windows.md:20` itself mandates for the shared window edge — and **12 are `Interface\AddOns\<Addon>\media\…` self-references**, neither of which the catalog is meant to replace. What is left is Blizzard chrome the ~30-mark catalog carries no equivalent for: ReadyCheck marks, the chat size-grabber, class circles, the casting-bar spark. | Both sites use `NS.Icon`; MultiMeters' parity comment is still true. Every remaining hard-coded path **in that scope** has a reason beside it or a register row covering its class. | M4-01 | S |
| **M4-24** | LootHistory, PrettyChat, BankLedger, WhatGroup | Make each `performance-§12` exemption page reproduce its own evidence. LootHistory: regenerate both tables (eleven events claimed against thirteen registered, `modules/Browser.lua:1277-1278` missing; four timers against five at `core/ItemSetup.lua:71`, `core/Util.lua:242`, `settings/OptionsSetup.lua:181`), drop the dead `Compat.lua:202` and `OptionsSetup.lua:129` citations, and rewrite `:45`'s `CHAT_MSG_LOOT` row — "one table insert" against `modules/Collector.lua:123-124`'s `C_TooltipInfo` build plus `GatherAll`'s three-addon cascade — re-affirming criterion (a) explicitly. PrettyChat: re-run the page's own grep, which now returns `settings/Panel.lua:528`, `:531`, `:532` against an assertion of zero, and give the one-shot `C_Timer.After(0)` a render-path disposition. BankLedger: repoint `:39` from `core/Compat.lua` to `core/ItemSetup.lua:67`. WhatGroup: amend the register row `M2-21` makes accurate. | Running each page's greps verbatim reproduces the tables printed on it, and every `file:line` resolves. **No exemption is withdrawn.** | M2-21 | M |

| **M4-25** | KickCD | **Clear the collection's one open complexity warning.** `tests/test_schema.lua:595-631` is a 29-NLOC anonymous function at **CCN 18**, and `automated-tests.md:143`'s release gate is `suites.complexity.warnings == 0`, so **KickCD cannot cut a tag while it stands**. Split it on the seam its own comment at `:613` names — the linked-Focus assertions and the unlinked-page counter are two cases, not one — keeping every assertion. This is `KICKCD-R-02`, which `05_TRACEABILITY.md` § 3b carried as unmapped; it is scheduled here because a Low that blocks a release gate costs something. | `lizard -l lua -x './libs/*' -x './tests/_kit/*' .` in KickCD reports **0 warnings**, against 1 today. `lua tests/run.lua` green with the case count up by exactly one, `docs/test-cases.md` and the README badge in the same commit. | M4-01 | S |
| **M4-26** | MultiMeters | **Disposition all 23 complexity warnings, one line each.** Measured today, every one is in shipped source — `core/` 5, `modules/` 15, `settings/` 3 — topping out at `scanColumn@1439-1540` (CCN 36), `Cell@646-726` (30), `NS.ReorderableBlocks@215-310` (28), `Export.ChatLines@535-600` (27), `Feign.Prune@227-285` (26) and `(anonymous)@1961-2032` (26). MultiMeters has never cut a tag and cannot while these stand. Each gets **split**, **accepted with a register row and a re-check trigger**, or **an open issue naming the seam** — and `scanColumn` gets a decision either way, because `M2-09` edits inside it. **No split lands in this plan**; the deliverable is the disposition, so `M5-01`'s "every watch-list entry carries a disposition" has something to resolve against instead of 23 blank cells. | Every one of the 23 rows the `M1-LK-07` watch list writes carries a disposition. `docs/ARCHITECTURE.md`'s register and `gh issue list` between them account for all 23. | M1-LK-07, M2-09 … M2-12 | M |

> **Correction (`M4c-03`), against shipped `393102f`.** This row's second acceptance grep was
> `RegisterWidgetType` over `core`, `modules` and `settings`, expecting nothing. In ConsumableMaster
> it returns four hits and always did: `modules/KCMIconButton.lua:145`, `modules/KCMScoreButton.lua:115`,
> `modules/KCMMacroDragIcon.lua:143` and `modules/KCMItemRow.lua:397`. None of them is residue. All four
> arrived in `bab4319` on 2026-07-12, two months before this cycle opened, and none was touched by the
> `core/LSMPatch.lua` deletion.
>
> The four register widget types this addon **owns** — `KCMIconButton`, `KCMScoreButton`,
> `KCMMacroDragIcon`, `KCMItemRow` — each declared local to the file that defines it, each version-guarded
> against its own name, each acquired by `AceGUI:Create` from `settings/Category.lua`, and all four pinned
> by `tests/test_widgets.lua`. Deleting them to satisfy the grep would delete the priority-row UI and
> redden six cases. `M1-STD-10` says the rule is about **where**, not **whether**, and `anti-patterns` #8
> sanctions `RegisterWidgetType` over forking a widget; a new name in the addon's own namespace is the
> sanctioned use.
>
> What `M4-04` … `M4-08` actually removed was a re-registration of `LSM30_Border` — a slot
> AceGUI-3.0-SharedMediaWidgets owns, which five addons were each overwriting at whatever version they
> found plus one. `RegisterWidgetType` is the mechanism the anti-pattern and the sanctioned use share,
> so on its own it cannot tell them apart: it is broad in exactly the way that makes a green acceptance
> meaningless and a red one an invitation to delete working code. The corrected sentinel keeps the call
> and adds the slot, because it is the pair that is forbidden.
>
> Grepping for `LSM30_Border` alone would not do either. `M4-02` put
> `lib.__PatchLSM30Border()` in `settings/OptionsSetup.lua` with sixteen lines of comment saying why the
> patch is a library act, and two of those lines name the slot: an acceptance reading "returns nothing"
> would go red on the very prose `M4-02` was asked to write. Measured in ConsumableMaster at HEAD, the
> corrected pipeline returns 0 lines and the four owned registrations stand.


**Safely parallel inside M4:** `M4-11` through `M4-26` touch different repositories and different files
and can run concurrently, subject to the one-lane-owner rule for `settings/OptionsSetup.lua`.
`M4-01` → `M4-02` → `M4-03` → `M4-04`…`M4-08` is a strict chain and must not be collapsed.

---

# M5 — the record and documentation tail

**Last, because everything above rewrites it.** `M1-LK-02` makes three of `C19`'s comments stale by
design — `AbsorbTracker/settings/Appearance.lua:121-129` says in as many words "delete this the re-vendor
after the fix lands". `C08`'s rows change on every run in M2, M3 and M4. `C14`'s registers gain a row for
each decline made above. Doing this tail early means doing it twice.

| ID | Repo | What changes | Verified by | Depends on | Effort |
|---|---|---|---|---|---|
| **M5-01** | all ten | Regenerate the automated-test record in each repo through `tests/_kit/run-automated-tests.sh`, which after `M1-LK-07` rewrites the standing prose above an existing header **and writes the complexity watch list and the four standing suite sections it never wrote before**. Every one of the ten is one to eight runs behind. **The line between generated and authored, which is what `M1-STD-07` rules on:** every figure, every table row and every watch-list entry is the runner's and is never hand-edited; the only authored cell is the watch list's **Disposition** column, written by the repository's owner and carried forward by the runner while the entry is unchanged. `M4-25` and `M4-26` supply KickCD's and MultiMeters' dispositions before this item runs. **No frozen bundle gains a file** — 35 of 93 bundles have no `ANALYSIS.md` and writing one today into a bundle stamped in August fabricates a record. The next run writes one and notes the gap once. | Each newest `RESULTS.md` row equals a fresh run; the row count equals `ls -d docs/automated-tests/*/ \| wc -l`; every watch-list entry resolves against a fresh `lizard` run and carries a disposition. Hand-editing any figure and re-running restores the runner's value. | M1-STD-07, M1-LK-07, M4-25, M4-26, M2, M3, M4 | L |
| **M5-02** | all ten | Sweep the deviation registers. Every cited audit ID resolves in `docs/audits/` — AbsorbTracker's `docs/ARCHITECTURE.md:354`, `:356`, `:357` cite `AT-A-10`/`AT-A-03`/`AT-A-09` against a bundle holding `AT-30`…`AT-50`. Retire rows whose triggers have fired (`LootHistory:392`, `WhatGroup:349`, fired 2026-08-06) and rows for collisions the standard has since resolved (`PrettyChat:222`'s `toc-file`/`layout` order, now identical at `toc-file.md:109` and `layout.md:53`; `ConsumableMaster:316`; `PrettyChat:230`, resolved by `M1-STD-05`). Add rows for the declines that live only in comments or closed issues: BankLedger's English-only and its close button, LootHistory's English-only and its issue #21. Close `WowAddonStandards#2`. | A case in each repo asserts every cited deviation ID resolves in `docs/audits/`. No row cites a rule the standard does not carry. No row's trigger has already fired. | M1-STD-03, M1-STD-04, M1-STD-05, M1-STD-15 | M |
| **M5-03** | KickCD, LootHistory, MultiMeters, PrettyChat, WhatGroup | The README and ARCHITECTURE structure. KickCD gains `## Overview` and `## Module map` — the only sibling without them — with inbound anchors and the map row moved. LootHistory promotes `README.md:36`'s `## Unreleased` third changelog into the next bump and folds `:141` into `## How attribution works`. MultiMeters spills its 787-line ARCHITECTURE (Known limitations and Overview to `scope.md`, Taint notes to `midnight-quirks.md`, Event subscriptions to `module-map.md`) and adds `audits/` and `reviews/` rows to its Topic detail table. PrettyChat moves `README.md:71-82`'s per-tab table to `docs/settings-panel.md` and adds `CLAUDE.md`'s adherence line. WhatGroup corrects `README.md:121` to Chat and collapses its settings table to page granularity. | Each `ARCHITECTURE.md` carries the mandated section names and every inbound anchor resolves. No addon README carries a third changelog surface. | M1-STD-03 | M |
| **M5-04** | AbsorbTracker, ConsumableMaster, MultiMeters, WhatGroup | Write the missing Tier 2 topic docs where the trigger has fired. `docs/compat-layer.md` for MultiMeters (761 lines, 31 shims), ConsumableMaster (83) and WhatGroup (130 lines, seven shims at `core/Compat.lua:24`, `:40`, `:52`, `:62`, `:83`, `:105`, `:125`); `docs/slash-dispatch.md` for AbsorbTracker (`PROFILE_VERBS` at `settings/Slash.lua:327`, dispatched `:386`, 17 verbs) and ConsumableMaster (`settings/Slash.lua:202` reads "seventeen verbs, five sub-command tables"). Flip each documentation-map row from Not applicable to Present. | Each repo carries the doc and its map row says Present. `M1-STD-14`'s threshold decides the marginal cases rather than an auditor's judgment. | M1-STD-14 | L |
| **M5-05** | AbsorbTracker, BankLedger, ConsumableMaster, LootHistory, MultiMeters, PanelMaster, PrettyChat | The comment sweep, roughly forty sites. Cite the **symbol** wherever the name is unambiguous, re-derive the genuinely positional citations. Named: ConsumableMaster's eight of fourteen (`core/DebugLogSetup.lua:93`, `:113`, `modules/MacroBarButton.lua:115`, `:146`, `tests/test_surface_parity.lua:84`, `:126`); AbsorbTracker's "fifteen appearance keys" against nineteen (`core/Units.lua:74`, `:108`) and the `CreateOptionsPanel` hazard the library now owns (`core/AbsorbTracker.lua:69` against `Options.lua:838-844`); LootHistory's `defaults/Global.lua:6-9` and `core/Database.lua:195`'s "v6->v9", and `modules/Browser.lua:1162`'s gap that `:1074-1077` already covers; PanelMaster's `Sl:CliResetAll`, which no file defines (`settings/OptionsSetup.lua:190-195`); BankLedger's `settings/OptionsSetup.lua:180-181`; the two vendor-sync comments quoting v1.8.3 and v1.10.2 against a live provenance line. **Plus the three comments `M3-03` and `M3-04` make stale by design.** | `/wow-addon:sync-docs`'s comment-citation check, added by `M1-WA-04`, reports nothing in the live tree. | M1-WA-04, M3, M4 | M |
| **M5-06** | all ten | Run `/wow-addon:standards-audit` fresh in each repository against the amended standard, and record what this plan actually closed. Two repositories entering the rotation for the first time under `M1-WA-06`. | Each repo holds a new `docs/audits/<date>/` bundle whose open-MUST count is reconcilable against `01_CONSOLIDATED_FINDINGS.md`. | M1-STD-16, M5-01 … M5-05 | L |
| **M5-07** | all nine addons, LibKa0s, WowAddonStandards | **File what this plan decided not to do, so the decisions outlive the bundle.** One `state:untriaged` GitHub issue per row, on the repository it belongs to, each linking this directory: the **seven findings with no work item** (`05_TRACEABILITY.md` § 3 — `BANKLEDGER-R-04`, `BANKLEDGER-R-07`, `LOOTHISTORY-R-16`, `PANELMASTER-A-03`, `WHATGROUP-R-04`, `WHATGROUP-R-06`, `WHATGROUP-R-12`), the **four deferred `C12` rows** waiting on kit 16 (`ABSORBTRACKER-A-10`, `MULTIMETERS-A-08`, `PANELMASTER-A-07`, `PRETTYCHAT-A-10`, all on LibKa0s as the kit's owner with the four consumers named), and the **eleven declines** in § *What this plan deliberately does not do*, filed as `state:will-not-do` with the argument copied rather than summarised. Without this the declines evaporate the moment the bundle closes and next cycle re-argues all eleven. Throttle the writes. | `gh issue list` in each repo returns a row for every entry above. Every issue body resolves to a `file:line` or to a named section of this bundle. | M5-06 | M |
| **M5-08** ⚠ | AbsorbTracker, BankLedger, LootHistory, PanelMaster, PrettyChat, WhatGroup | **Write the non-English-client section into the six `docs/smoke-tests.md` files that have none**, in the shape `M1-WA-05` scaffolds for new addons — `M1-WA-05` edits `commands/new-addon.md` and nothing else, so without this item the gap is fixed only for addons that do not exist yet. The two that need it most are named: LootHistory, whose `core/Compat.lua:188-195` defines four English wordings as the fallback when the client leaves `ITEM_ACCOUNTBOUND*` nil and whose every headless case asserts against enUS mock globals; and PrettyChat, whose entire function is overwriting localized `_G` chat format strings across 797 lines of smoke doc with no locale step. This item also **owns session 6** — it schedules the pass, and its recorded outcome is what `WHATGROUP-R-06` has been waiting on. | Each of the six carries a locale section naming what to look at and what a failure looks like. Session 6 has been run once and its result is recorded, including the `C_SpellBook.IsSpellKnown` observation `WHATGROUP-R-06` needs. | M1-WA-05 | M |
| **M5-09** | PanelMaster | **The ruling `PANELMASTER-A-03` needs, and then the rows.** `03_SPEC.md` § `C30` asks that each remaining hand-written group either composes or carries a register row with a re-check trigger, and no item made the call. The call, per the owner's decision 4: **register rows, not a composer arm.** A composer arm for record-backed binds is an upstream Options change, and this cycle cuts two LibKa0s tags whose contents are already fixed — adding a third surface to carry one addon's hand-written groups is the tail wagging the dog. Write an `options-ui-§16` register row per remaining group, each naming the record-backed bind as the reason and carrying a re-check trigger tied to the next Options major. **This does not close the underlying question**; it records it where the next audit will see it. | Every hand-written group in PanelMaster either composes or has a register row with a trigger. `M5-06`'s fresh audit reports no `options-ui-§16` deviation. Satisfies the last of § `C30`'s five acceptance criteria. | M1-STD-11, M5-02 | S |
| **M5-10** | WhatGroup | **`WHATGROUP-R-06`, after session 6 has answered it.** `core/Compat.lua:62-67` calls the bare `IsSpellKnown` global and returns false when absent, while its five siblings at `:24`, `:40`, `:52`, `:83` and `:105` all try `C_Spell.*` first. Add a `C_SpellBook.IsSpellKnown` rung above the global, in the shape the siblings use. **Gated, not optional:** the finding's own fix text conditions the change on an in-client check confirming both APIs present and agreeing, `06_SMOKE_TESTS.md` § 6.3 carries that check, and `M5-08` runs it. If session 6 reports the two APIs disagreeing, this item does not ship a rung — it records the disagreement and files it, which is a different outcome and an acceptable one. | Session 6's recorded result is cited in the commit. A case asserts the `C_SpellBook` rung is tried first and the global remains the fallback. `core/Compat.lua`'s six accessors have one shape. | M5-08 | S |

---

# In-client smoke sessions

Seventeen of the eighteen `⚠` items above belong to one of these five sessions; the eighteenth is
`M5-08`, which owns session 6. Batching them is deliberate: each costs a login,
several need combat, and one needs five addons loaded at once. Running them item by item across five
milestones costs a login per item and finds nothing extra.

**Session 1 — combat and taint.** After M2 Lanes E and F. Enter combat and, from the Blizzard AddOns
sidebar, open AbsorbTracker, KickCD and MultiMeters — expect the refusal message and a closed panel
(`M2-16`, `M2-17`, `M2-18`). `/reload` in combat with ConsumableMaster loaded, expect no taint error and
the category registering on regen (`M2-08`). Invoke WhatGroup's reset popup in and out of combat, watching
for "Interface action failed because of an AddOn" (`M2-20`). Enter combat with WhatGroup's frame shown and
confirm it hides; leave with a pending invite and confirm it returns (`M2-21`). Apply to two
group-finder listings and let both resolve, one accepted and one declined; `/bl` reset everything then
capture a bank movement without reloading; `/kcd` debug dump with and without `C_CurveUtil` (`M2-22`).
`/mm debug of` — expect a rejection line, not a report (`M2-11`).

**Session 2 — SavedVariables.** After M2 Lane B, on a **copy** of the account's SavedVariables, never the
live file. BankLedger: drop `schemaVersion`, add a `vendorPrice` row, log in, expect
`v1 -> v2, 1 rows touched`, log out, confirm the stamp persisted (`M2-05`). ConsumableMaster: create and
switch to a second profile, confirm the migration line fires — it does not today (`M2-07`).

**Session 3 — panels and pooling.** After M2 Lane A and M4's panel items. Open PrettyChat's landing page,
page to another addon's settings, confirm no 300px logo rides through (`M2-02`). `/pm` → Panels, confirm
the five acts sit in the chrome band and each works (`M4-15`). `/at perf`, `/kcd perf`, `/mm perf`, each
with one close button in the same place (`M4-16`). Then the tab strip: after `M4-01`, open every
multi-tab settings panel in each of the nine addons, cycle its tabs three times, and confirm labels,
selection state and band height are unchanged (`M4-01`) — `M1-LK-03` makes tab buttons and the content
panel pooled and re-dressed, `TabStrip` renders in the live settings code of all nine, and the only
headless proof counts `CreateFrame` calls.

**Session 4 — the media dropdowns.** After `M3-01`, before `M3-02` opens. `/kcd config` → Icons, Label,
Castbar: every font, border and bar-texture dropdown lists real media names.
`/dump LibStub("LibKa0s-Options-1.0").MODULES.OptionsCompose` reports 3. Then, after `M3-02`, open a
MultiMeters media dropdown once a media addon has registered a face and confirm the face is listed —
that is the check that catches the `__AttachCompose` contract change if the revert was missed.

**Session 5 — the shared widget registry.** After `M4-02`, and again after **each** of `M4-04` …
`M4-08` — six runs, which is what the five separate deletion commits were bought for: a failure names
one repository instead of one range. Load KickCD,
PanelMaster, AbsorbTracker, ConsumableMaster and MultiMeters together and open each addon's Border
dropdown in turn. Every one draws the same styled control, and the styling does not depend on load order.
This is the only proof `C02` has; a headless suite cannot see the interaction at all.

---

# Branches, merge order, and where the record goes

Ninety-five of the hundred items land in a repository, thirteen repositories are in play, and M1 and M2
run in parallel from day one. Nothing above says where those commits go, and every previous bundle in
this directory answered that before it started.

**One branch per repository, named `feat/2026-09-07-audit-review-remediation`.** The same name in all
thirteen, so `git log --oneline` in any of them is filterable by the same string and a cross-repo state
question is one loop. Every commit subject opens with its item id (`M2-09: …`), which is what makes the
bisect points in `M4-04` … `M4-08` and the failure map in `06_SMOKE_TESTS.md` § *If a step fails* usable.

**Merge order is forced by the payload, not by preference.**

1. **LibKa0s and WowAddonStandards merge first**, in either order, and before any addon branch merges.
   A tag cut on an unmerged branch is a tag on a commit that may not survive review; `M1-LK-04` and
   `M1-LK-15` are the two places this matters.
2. **`wow-addon` merges whenever it is ready.** It is docs-only and nothing consumes it mechanically.
3. **The nine addon branches merge after `v1.27.0` exists**, except that an addon whose branch holds
   only M2 work may merge as soon as its own suites are green — M2 depends on nothing, and holding it
   behind the tag is the sequencing error this plan's milestone map warns about.
4. **`M4-04` … `M4-08` merge in their stated order**, one repository at a time, with the session-5 smoke
   between each. Merging them as a block discards the five attribution points they exist for.

**The record is written afterwards, in this directory, as `07_EXECUTION_RECORD.md`.** Not now: this
bundle's first page says nothing here has been run, and that stays true until it is not. Every prior
cycle wrote one — `docs/2026-08-05-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/06_EXECUTION_RECORD.md`
records 201 commits across eleven repositories, on a named branch, with a *what is not done* section —
and the correction belongs beside the claim rather than inside it. The other seven documents are the
record of what was intended and are not rewritten.

---

# What this plan deliberately does not do

Each of these was proposed by a finding or a cluster disposition, examined, and declined. They are listed
so the decision is recorded rather than re-argued next cycle.

**Rebind `lib.MakeCloseButton`.** Payoff is roughly 24 lines across eight three-line wrappers. Cost is a
signature change to a surface all nine consumers vendor, forcing a re-vendor wave for cosmetics — and it
is contradicted by the library's own reasoning at `LibKa0s/Media.lua:14-20`, which records that `...`
carries the addon folder name only for a file the TOC loads directly, so the library cannot infer it. The
cheap close is `M1-STD-04` plus one BankLedger register row in `M5-02`. Note also that the ledger's
"BankLedger and LootHistory declined" is one release stale: `LootHistory/core/CoreSetup.lua:167` wraps it
correctly, and `:19-25` records that its old decline "expired with LibKa0s v1.10".

**Split any file for the 1500-line cap.** `M4-14` dispositions them; it splits none. This is a MultiMeters
problem — seven source files and seven test files — and MultiMeters is also the repository carrying the
feign-trace subsystem in `modules/`. Splitting `settings/Schema.lua` (3069) and `modules/Window.lua`
(2644) is the largest mechanical churn available here, has no player-visible payoff, and collides head-on
with the one cluster in that repo that does. If ever, only after `M2-09` … `M2-12` have landed.
`PrettyChat/GlobalStrings/GlobalStrings.lua` at 23,842 lines is generated, unloaded and
`.pkgmeta`-ignored, and is exempted by rule in `M1-STD-08` rather than split.

**Backfill `ANALYSIS.md` into the 35 frozen bundles that lack one.** They are dated, frozen records.
Writing an analysis today into a bundle stamped in August fabricates one. `automated-tests.md:245` only
MUSTs the write-up for release runs in any case. Fix forward.

**Rename the `minimise` icon key.** `lib.Icon` (`Media.lua:207`) builds the path *from* the key and
`minimise.tga` is the file on disk in ten vendored trees, so adding `"minimize"` to `lib.ICONS` alone
yields a path to nothing — the silent failure `Media.lua:190-196` itself records. `M1-LK-11` fixes the
prose and the player-facing chat strings and leaves the key, with a register row.

**Annotate every TOC line.** `CX04` as filed measures `toc-file-§5:144`'s MUST against all 23–81 lines of
nine files. The MUST binds only load-bearing positions, and against that denominator it is `M4-12`'s
eight one-liners. `AbsorbTracker.toc:39-40` is already a compliant instance. A MUST that no repo satisfies
is worth checking against its own text before it is worth nine repositories of work.

**Turn on linting for 308 test files in one step.** `M1-LK-12` proves the config shape in LibKa0s,
`M1-STD-01` puts it in the template, and only then does `M4-11` propagate it. Flipping all ten at once
produces a wall that gets silenced with a blanket ignore, which reads as coverage and provides none —
worse than the exclusion it replaced.

**Flip the shared mock's `GetHeight` in this plan.** `M1-LK-08` is additive and stops there. Roughly 308
test files across ten repositories lean on geometry answering zero, and every assertion that passes today
*because* of that flips with it. Kit 16 is a later tag, after each consumer has adopted the opt-in.

**Publish a no-op Options surface from LibKa0s.** It would have to live in the payload that is by
definition absent on the path the stub exists for — `AbsorbTracker/settings/OptionsSetup.lua:44` opens
`local lib = LibStub and LibStub("LibKa0s-Options-1.0", true)` and the stub is the arm below it.
`M1-LK-09` moves the work kit-side instead.

**Withdraw any `performance-§12` exemption.** All four survive on merit; `M4-24` repairs their evidence
and nothing else.

**Ship a `RESULTS.md` figure by hand.** Every number in that file is the runner's. A hand-edit is the
defect `C08` is about, not its fix.

**Cut any release beyond `v1.26.0` and `v1.27.0`**, plus whatever standard version the `M1-STD-16` rollup
lands as. No addon version bump is specified anywhere in this plan.
