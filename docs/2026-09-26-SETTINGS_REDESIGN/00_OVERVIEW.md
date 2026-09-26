# AuraMaster settings redesign (#6): overview

**Status: DRAFT, not executed.** Nothing in this bundle has run. `feat/2026-09-26-settings-redesign`
exists only in AuraMaster (it carries the spec, `3fdc667`); WowAddonStandards and LibKa0s have no such
branch yet. Nothing is committed or pushed, and the bundle itself is not committed. It is frozen once
execution starts (`../../CLAUDE.md`, "Bundle conventions").

The design is frozen by the owner ("Lock it in!", 2026-09-26). It lives in the spec at
`../../../AuraMaster/docs/superpowers/specs/2026-09-26-settings-redesign-design.md` (relative to this
bundle; `$GIT/AuraMaster/…` from anywhere), on AuraMaster's branch
`feat/2026-09-26-settings-redesign`. Read the spec first; this bundle only turns it into work.

## Why the plan lives here

The spec's status line says the plan goes under AuraMaster's `docs/superpowers/plans/`. The work
touches three repos, though: a WowAddonStandards rule, a LibKa0s release and the AuraMaster change.
`../../CLAUDE.md` puts cross-repo work in a dated bundle here, so this bundle holds the plan. AuraMaster
keeps only the spec.

## What the owner decided (from the spec)

| # | Decision | Spec | Where it lands |
|---|---|---|---|
| D1 | The Filters, Layout, Bars, Icons and Text sub-pages fold into **Containers**, one config page per container, built from the container's type. The tree becomes General · Containers · Profiles. | §1, §3 | SR-AM-03, SR-AM-05 |
| D2 | **Test10 (Pinned nav)** from the lab (`lab/2026-09-26-settings-layout`, `d0d0196`, `settings/LayoutLab.lua:665-830`) is the design. The other nine Test pages are rejected. The lab is never merged. | §2 | SR-LK-01 (rail), SR-AM-03 |
| D3 | Two visibly different levels. The first is a pinned nav rail on the left, **120px**, in the AceGUI TreeGroup tree-pane look, with entries General · Filters · Layout · <style>. The second is the library's own pinned primary `TabStrip`, in the right column only. | §2 | SR-LK-01, SR-AM-03 |
| D4 | Only the scroll moves. It is the page's own AceGUI scroll, with no height cap, so every library widget draws as it does today. | §2 | SR-LK-01 (inset), SR-AM-03 |
| D5 | The rail's top is level with the **top of the tab art**, not the top of the tab button. It is measured at draw time and never hard-coded. | §2, §4 | SR-LK-01 |
| D6 | The style entry is **one** entry, for the container's own style. The disabled-for-this-style notice goes. A Style change heals an active style entry to the new style's. | §3 | SR-AM-03, SR-AM-05 |
| D7 | The schema is unchanged. A section is a former page key, so `/am set`, `/am get`, `/am list`, defaults and every row path stay as they are. | §3 | SR-AM-02 |
| D8 | `ctx.activeSection`, plus `ctx.activeTab` kept per section. Both are session state and never persisted. | §3 | SR-AM-03 |
| D9 | Defaults restores the **active section's** rows for the selected container. On General that is Enabled, Unit, Aura type and Style, and `noReset` on the name still holds. | §3 | SR-AM-04 |
| D10 | The library gains the seam. `O.NavRail(ctx, spec)` goes into a new Options minor, with draw order **PageBanner → NavRail → TabStrip** and one `__railInset` read by the strip, the content panel and the scroll. Rail width 0 is byte-identical to today. | §4 | SR-LK-01 |
| D11 | The standard gains the rule. options-ui-§13 sanctions the rail as a first level, and "no third level" stands. In options-ui-§14 the band sits above both the rail and the strip, and the rail is not a picker. | §5 | SR-WS-01, SR-WS-02 |
| D12 | Deep links keep `NS.OpenOptionsPage(pageKey)`. A former sub-page key opens Containers on that section. | §6 | SR-AM-04 |
| D13 | Out of scope: the General (addon) page, Profiles, any change to what a setting does. Bars' seven tabs wrap to two rows at 473px, and IdList drops to one column there. Both are accepted. | §7 | — |
| D14 | Execution order (task instruction): standard and library first, then AuraMaster. LibKa0s is released as a **local** tag `v1.61.0` and not pushed. No addon version bump. Pushes happen only if the owner authorizes them at plan review, and nothing is ever merged. | — | all |

## Needs the owner's sign-off at plan review

The spec is frozen, so a plan resolution that changes how a spec requirement is met, and not only
fills a gap, is the owner's to accept. Two decisions are asked before SR-LK-01 starts. Both answers are
recorded in the M1 row of `checkpoints.tsv`.

| # | Question | Plan's proposal | If declined |
|---|---|---|---|
| O1 | Spec §2 and §4 say the rail's top is "measured after the strip is drawn … from the drawn tab's textures". May the library measure the selected tab's atlas (`Options_Tab_Active_Left`) on a hidden probe instead, before the strip exists? | Yes (A2 in `03_EXECUTION_PLAN.md`). The outcome is the same: the rail's top is level with the tab art's top, measured and never hard-coded. The library already rules reading art back off a drawn tab a defect (`LibKa0s/OptionsTabs.lua:380-383`), and a test pins the probe's number to the drawn selected tab's art. | SR-LK-01 takes A2's fallback: `placeTabs` calls `lib.__alignRail` with the drawn first row's tallest art after placing the tabs. |
| O2 | Pushes: may the M1 and M2 checkpoints push the feature branches and `refs/notes/ka0s-review` (never a tag, never a merge)? | Owner's call (D14) | Nothing is pushed. `/wow-addon:finalize` pushes later. |

## Scope

| Repo | What it gets | Milestone |
|---|---|---|
| WowAddonStandards | v2.69.0: options-ui-§2, §13 and §14 name the nav rail. The ripple goes to STANDARDS.md, EXECUTIVE_SUMMARY.md, NEW_ADDON_CONTEXT.md, AUDIT.md, library-stack.md and README.md. | M1 |
| LibKa0s | v1.61.0: a new `OptionsNav.lua` (OptionsNav minor 1) carrying `O.NavRail` and `lib.__railInset`; guarded call sites in `Options.lua` (minor 25) and `OptionsTabs.lua` (minor 5). The Options key becomes **25.31.5.7.4.1**. Local tag only. | M1 |
| AuraMaster | Re-vendor v1.61.0, then the section registry and the Containers page with its rail, deep links and Defaults. After that the sub-pages retire (D6 goes), then tests and docs. | M2 |
| Ka0sAddonsCommonTasks | `99_REPORT.md` and `checkpoints.tsv` rows. The owner's smoke results go in `06_SMOKE_TESTS.md`. | M3 |

**Not in scope: MultiMeters (#55) and KickCD (#33).** Each is filed as its own GitHub issue citing the
spec, and each depends on this plan's M1 (the library minor and the standard change). The owner's
instruction is "fix AuraMaster first, then do similar to MultiMeters and KickCD". Neither addon is
touched here, and neither is re-vendored to v1.61.0. The other nine hosts also stay on LibKa0s v1.60.0,
as v1.59.0 was re-vendored into AuraMaster alone (`../LibKa0s/docs/releasing.md`, "Every step 8"). When
they take v1.61.0, each host's library-absent stub gains a `NavRail` no-op, and SR-LK-01 (Step 7)
records that in the v1.61.0 CHANGELOG block's "What a consumer owes" section. PanelMaster#55 is closed `state:will-not-do`.

The D6 nesting mark (`NS.SubPageLabel`) is an AuraMaster and MultiMeters design note, not a rule in the
standard. `grep -rn "SubPageLabel\|D6" ../WowAddonStandards` finds nothing. So spec §5's third bullet
needs no edit to the standard. AuraMaster drops its copy in SR-AM-05. MultiMeters keeps its own copy
until #55.

## Milestones

| Milestone | Repos | Content | Checkpoint |
|---|---|---|---|
| **M1** | WowAddonStandards, LibKa0s | SR-WS-01 and SR-WS-02 run in parallel with SR-LK-01 and SR-LK-02. Then SR-LK-03 releases v1.61.0 (the local tag), because its README pointer needs v2.69.0. | WS: the docs gate over the changed .md files. LK: the release battery (`--release 1.61.0`) is green and `v1.61.0` exists locally. Both branches are pushed only if the owner authorized pushes. |
| **M2** | AuraMaster | SR-AM-01..SR-AM-06, in order, one at a time | Full green gate (tests 0 failed, luacheck 0/0, lizard 0 over CCN 15, vendor == v1.61.0), clean tree, branch pushed only if authorized |
| **M3** | Ka0sAddonsCommonTasks | SR-REC-01 | `99_REPORT.md` and the checkpoint rows on `main` |

## Dependency order

```
SR-WS-01 options-ui rule ──► SR-WS-02 ripple ─────────────────────┐
                                                                   ▼
SR-LK-01 OptionsNav + seams + tests ──► SR-LK-02 prose ──► SR-LK-03 release v1.61.0 (local tag)
                                                                   │
                                                                   ▼
SR-AM-01 re-vendor ─► SR-AM-02 sections ─► SR-AM-03 rail page ─► SR-AM-04 deep links + Defaults
                                                                   │
                                                                   ▼
                                  SR-AM-05 retire sub-pages ─► SR-AM-06 docs ─► SR-REC-01 record
```

## Files in this bundle

| File | What it is |
|---|---|
| `00_OVERVIEW.md` | This file |
| `03_EXECUTION_PLAN.md` | The implementation plan: global constraints, review focus, every task with its files, interfaces, test code, implementation code, commands and commit |
| `items.tsv` | The manifest: id, milestone, repo, title, dependencies, effort, smoke checks, traces |
| `resume-state.sh` | Progress computed from git (zsh, read-only) |
| `RESUME.md` | How a fresh session picks the run up |
| `checkpoints.tsv` | One row per milestone that passed its checkpoint (header only until then) |
| `06_SMOKE_TESTS.md` | The owner's in-client checks: spec §8 plus the ones this plan adds, each with an empty Result |

There is no `01`/`02` pair. The findings are the spec and the four read-only surveys that fed this
plan (the LibKa0s, AuraMaster, standard and lab maps). Their facts are cited inline in
`03_EXECUTION_PLAN.md` with file:line.

## After this bundle (owner, 2026-09-26)

This bundle is AuraMaster only, with LibKa0s v1.61.0 as a LOCAL tag. Once AuraMaster is done and
accepted, the owner's sequence is: push LibKa0s (master and the v1.61.0 tag, with the owner's
go-ahead), merge the standard's v2.69.0 branch, re-vendor LibKa0s v1.61.0 into every addon, then
build the same layout in MultiMeters (MultiMeters#55, the Windows page) and KickCD (KickCD#33, the
Grid page). That is a new bundle.

Execution note: the owner waived review of the spec and this plan and asked for the build to run
("go ahead and build the settings redesign without my approval on spec or plan", 2026-09-26).
Pushes of feature branches were not authorized, so checkpoints record evidence without pushing.
