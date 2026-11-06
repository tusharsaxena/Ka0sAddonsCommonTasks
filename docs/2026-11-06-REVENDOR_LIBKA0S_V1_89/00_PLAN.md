# LibKa0s v1.89.0 re-vendor across the collection (2026-11-06)

Run of `/dev-copilot:wow-revendor-libka0s all`, with the owner asked to check what the new library
surfaces offer each addon. Branch in every touched repo: `feat/2026-11-06-revendor-libka0s-v1-89`.

## Scope

`ls -d ../*/libs/LibKa0s` lists 17 consumers, and every one is on the roster in
`../WowAddonStandards/standards/ADDONS.md`. Library tag **v1.89.0** (`0bd4839`, pushed, tree clean).

| Base | Addons |
|---|---|
| v1.85.0 | AbsorbTracker, AuraMaster, BankLedger, ConsumableMaster, DpsRace, KickCD, LibKa0sSkinTester, LootHistory, MultiMeters, PanelMaster, PartyFrameEnhanced, PremadeGroupsFilterExtension, PrettyChat, WhatGroup |
| v1.86.0 | QuickComms |
| v1.88.0 | DropWatcher |
| v1.89.0 | OutfitterReborn (already current: verify only, `V89-OR` in `exceptions.tsv`) |

Step 0 pre-flight is in `inputs/step0-preflight.txt`. Every row reads `ok` except DropWatcher, whose
`2026-11-05-v1.88.0` bundle states base v1.85.0 while the provenance line before `59e323d` named v1.87.0
(the mislabelled untagged toast-stack tip, which that bundle itself explains). `V89-DW`'s `01_DELTA.md`
carries the one correction paragraph.

The skill's Step 0 roster regex (`\]\(\.\./\.\./…/\)`) matches nothing, because ADDONS.md now writes its
folders as backticked paths (`` `../../AbsorbTracker/` ``). The run used `` `\.\./\.\./[A-Za-z0-9]+/` ``.
This is a dev-copilot spec defect, reported in `99_REPORT.md`.

## The delta, v1.85.0..v1.89.0

| Tag | What moved | Class |
|---|---|---|
| v1.86.0 | New major `LibKa0s-IconBrowser-1.0` (three files at 1); DebugLogDiagnostics 6 -> 7 (the report names IconBrowser) | C (IconBrowser) / A (diagnostics) |
| v1.87.0 | Widgets 22 -> 23: `W.ContextMenu` rows gain `submenu`, `radio`, `selected`, `opts.check`. Flat menus draw what 22 drew | B / A |
| v1.88.0 | Toast 3 -> 4: the opt-in stack. A host's Toast stub gains `SetStack`, `Visible`, `FrameFor` | B / stub owed at re-vendor |
| v1.89.0 | Kit 50 -> 51: the CallbackHandler unregister guard (a flake fix) | A |

No `NEEDS_*` floor rises. No `__` member was removed, so no dead stub mirror is expected (each item
still greps for one).

## Decisions (owner, 2026-11-06, asked upfront)

| Candidate | Addon | Decision | Item |
|---|---|---|---|
| Widgets 23 `submenu` rows instead of reopening one level in place (`core/WidgetsSetup.lua:38-90`) | DpsRace | **adopt** | V89A-DR |
| Widgets 23 `radio` + `selected` tick on the skinned segment menu (`modules/Window_Header.lua:1212`, comment at :1281) | MultiMeters | **adopt** | V89A-MM |
| Widgets 23 cascade for the compact Filters ▾, replacing the Filters panel (`modules/CompactChrome.lua:21`, "WHY A PANEL, NOT SUBMENUS") | DropWatcher | **adopt** | V89A-DW |
| Toast 4 stack | DpsRace | settled (one toast at a time, library CHANGELOG v1.88.0) | none |
| IconBrowser | every addon without an icon chooser | settled, recorded in each bundle, **no issue** (owner ruling) | none |
| Cascading-menu fields | addons with no `W.ContextMenu` use site | not applicable, recorded in the bundle, no issue | none |

Declines: the owner ruled that **issues are filed only for real not-now candidates**. With every real
candidate adopted, the run expects to file no issue. An item that finds a genuine candidate this table
does not name stops on it and reports it to the lead, who decides. It never implements or files on its own.

## Per-item procedure (M1, `V89-<X>`)

The skill's Steps 3–4 and 8, in the addon's repo, on the branch:

1. 3a–3j into `docs/revendor/2026-11-06-v1.89.0/01_DELTA.md` **before** the copy (line 1
   `Delta: LibKa0s <base> -> v1.89.0`), including the 3h span check (a span bundle only if it prints).
2. Copy both payloads whole from `git -C ../LibKa0s archive v1.89.0 LibKa0s testkit tools`; content
   diffs empty; roll the provenance line and keep the `LibKa0s icons:` line; run the tag's
   `tools/prune-icons.lua`; README credits in step if a set changed.
3. Blockers in the same commit (DpsRace: Toast stub gains `SetStack`, `Visible`, `FrameFor`).
4. `02_CANDIDATES.md`, `03_DECISIONS.md` (decisions from this plan, no interview), `05_SUMMARY.md`.
5. Gate: `ka0s-bounded luacheck .` 0/0 and `ka0s-bounded lua tests/run.lua` green, 1500-line cap.
6. One commit: `V89-<X>: Re-vendor LibKa0s v1.89.0` (the bundle with it). Unrelated red stops the item.

## Adoptions (M2, `V89A-<X>`)

Each one gets a characterization test first, an assertion on what is drawn (rows, ticks, submenu
structure) and not only that the code runs, the gate green, and its own commit. Fence 5 applies: a new
catalog name drawn is declared in the same commit and the prune re-run.

- **V89A-DR**: `NS.OpenMenu` records the `fill` as before, but hands `W.ContextMenu` one tree in which a
  button with a nested level becomes a `submenu` row. `showLevel`'s in-place reopen and the hand-drawn
  `chevron-right` mark go, because the library draws the arrow. Retire `chevron-right` from the
  declaration only if nothing else draws it. The no-library MenuUtil path is unchanged.
- **V89A-MM**: the segment rows gain `radio = true` and `selected` (the existing `isActive` predicate),
  so the shown segment is ticked. The client fallback stays as is, apart from fixing its stale comment if it
  only described the missing tick.
- **V89A-DW**: Filters ▾ opens `W.ContextMenu` with one `submenu` row each for Quality, Content,
  Character and Sort. Each child lists that dropdown's own options with `selected` read from the
  **same** dropdown state (one state, as the panel guaranteed), multi-select picks `keepOpen`, and Sort
  is `radio`. The button's count label and its tooltip are unchanged. The panel's frame, its outside-press
  listener and the dropdown reparenting go. The file comment's "WHY A PANEL" paragraph is rewritten to
  record the cascade. The full layout's bar is untouched.

## Milestones and checkpoints

- **M1**: every `V89-*` committed, independently verified (`refs/notes/ka0s-review` note per repo), then
  the branches pushed. Row in `checkpoints.tsv`.
- **M2**: the three `V89A-*` committed and verified, then pushed. Row in `checkpoints.tsv`.
- **Owner smoke**: `06_SMOKE_TESTS.md`.
- **M3, on go-ahead**: `/dev-copilot:finalize` merges `--no-ff` in every touched repo, pushes master,
  deletes the branches (local and remote) and any worktree or stash this run made. `V89-FIN` records it.

No version bumps, no tags (the library tag already exists and is pushed).
