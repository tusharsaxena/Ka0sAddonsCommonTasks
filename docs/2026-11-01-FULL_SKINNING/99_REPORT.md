# Report: full skinning

**No smoke has passed. The v1.85.0 tag is local only.** `git ls-remote --tags origin v1.85.0` prints nothing; the tag sits at LibKa0s `2ad1a50`. Nothing is merged, no version is bumped. M1 and M2 are pushed. M3 is committed in every repo and not pushed. `WowAddonStandards` has no remote branch for this run at all.

## Outcome against the goal

Goal (`00_PLAN.md`): change the skin and every Ka0s addon changes with it, uniformly.

- **In the headless suites, the goal holds.** All 16 addons wire the kit's `test_skin_switch` (each declared painted surface must change under a probe skin) and `test_skin_values` (typed colors and textures need a named cause). Every suite is green; see Test totals.
- **In the game, the goal is unproven.** A probe skin gives every token its own value; the shipped skins are what you will see. Only your smoke can confirm them, and several things only a client can prove are listed under Known limits.
- **Run state.** `./resume-state.sh` prints `OPEN FS-REPORT` and `TOTAL 79/80` before this commit. Seven FLIP items owed no work and are exceptions in `exceptions.tsv`; the five with a count proof were re-run and print 0. `resume-state.sh` does not see the `FS-<p>-GATE` commits or LibKa0s's `FS-FIX` commits, because neither is in `items.tsv`.

## What shipped

**M1, the library** (checkpoint 2026-11-01 12:20). FS-L1 to FS-L9, FS-D1, FS-T1, FS-A4 and FS-REL in LibKa0s: launcher and tooltip text, settings chrome, fonts and typed colors with the Scope cleared, Ka0s marks, scroll arrows, title bars, composer defaults, new HUD tokens, and the delete confirmation for our own use of it.

**M2, the addons** (checkpoint 16:58). `FS-<p>-RV`, `-FLIP`, `-FIX`, `-REC` in all 16 addons: colors, shadows, borders and glow moved onto the skin with a one-time migration per profile, plus the host fixes for A1 to A3 and A5. QuickComms also took issues #13 and #14. DpsRace also holds the 42-dummy catalog (`09f02e7`), the 10 s toast (`1b9d003`) and the sound selector (`fdb6f5d`).

**M3, the gaps and the gate** (no row in `checkpoints.tsv`, not pushed).

- LibKa0s `430354d`: every skin states its own `bar.bg`, `bar.border`, `icon.border`, `glow.color` and `cover.dim`; four skins state a real `bar.borderStyle`; a skin's None defers to the stored style and Show border; `W.ContextMenu`; `S.HudFont` one font object per look with `opts.shadowToken`; `S.IconBorder` on a Texture; numeric path segments; `S.HoverArt`.
- LibKa0s `97a46c6` (FS-GATE): kit revision 50, the two suites above.
- LibKa0s `95b5252`: the Solid border registered with LibSharedMedia, menu and gate fixes.
- WowAddonStandards `553bc77` (FS-WS): skinning-§9 and skinning-§6, standard v2.97.0, anti-pattern #110.
- Every addon: an `FS-<p>-GATE` commit re-vendors the re-cut tag and adopts the gate.
- QuickComms `ec820e9` and `32bf98d`: your in-game pad findings, merged onto the re-cut library.

## Owner rulings taken during the run

| Ruling | Where it landed |
|---|---|
| Each skin has its own bar background, bar border, icon border and glow; Ka0s Default unchanged | `RESUME.md`, LibKa0s `430354d` |
| A skin's None bar border defers to Show border and the stored style; a real style wins | `RESUME.md`, LibKa0s `430354d`, the hosts' GATE commits |
| The KC, AM and DW migration overrides are accepted | `RESUME.md` |
| The Ka0s Default look moves stay, named on the smoke list | `RESUME.md`, `06_SMOKE_TESTS.md` section 3 |
| Animations are for the dial only, not the pads | QuickComms `b58e642` |
| Rotate and scale is the default open and close | QuickComms `93e1ce0`, spec line 29 |
| Scale and fade is removed | QuickComms `93e1ce0`, spec line 29 |
| Animation duration 0.1 to 2 s in 0.1 s steps | QuickComms `f551696`, `settings/SchemaMembers.lua:899` |
| Ka0s Default's pad buttons take the fuller look, over the keep-pixels rule | QuickComms `ec820e9` |

The plan's own rulings are in `00_PLAN.md`.

## Gaps

Left open:

| Gap | Why | Evidence |
|---|---|---|
| BankLedger `tab.glow` (row 150) | `S.Tab` only tints a glow a host draws, and these tabs have no hover glow. Adding one is a new feature | `modules/Browser.lua` has no glow |
| DropWatcher boxes (row 269) | `S.Card` paints them, but `card.*` has no style or size token, so no new look | `modules/DetailCard.lua:115` |
| DropWatcher footer band (row 274) | The band fills `footerHost`, inset from the body, so it is not full width | `modules/Window.lua:484-487` |
| SkinTester footer height (row 37) | No token exists, so 22 stays typed. Title and scroll width do read tokens | `modules/Showroom.lua:34-35` |
| SkinTester background and sound samples (row 49) | No skin token names either | `settings/Schema.lua:294-301` |
| LootHistory disabled menu labels (row 361) | Stay `text.disabled`; no disabled menu token exists | `modules/BrowserTable.lua:1077` |
| MultiMeters segment picker in combat (row 394) | Under the Combat restriction a label can be a secret string, so the client's menu stays there | `modules/Window_Header.lua:1223-1226`, `a5de38b` |
| QuickComms window fill (row 558) | A window fill has no texture token, so it stays flat. The map row said so | `modules/Pad_Render.lua:411` |
| `S.SquareIcon` in the SkinTester (row 9) | Always draws a flat 1 px `icon.border` edge, so under a None icon style the sample still shows one | `LibKa0s/SkinPaintControls.lua`, `prim.SquareIcon` |

Closed by M3:

| Gap | Closed by |
|---|---|
| DpsRace had no gloss (it has no A3 row, and the triage put it under A9) | `5bfa6e5`: the bars take `S.BarGloss`; check SM-DR-FS17 |
| DpsRace, MultiMeters and PGFE menus had no library surface | LibKa0s `430354d`, then `5bfa6e5`, `a5de38b`, `e638513` |
| PGFE lost per-entry tooltips and the divider | `e638513` |
| Skins shared one bar, icon and glow value, so D4 and D5 barely moved | LibKa0s `430354d` |
| `bar.borderStyle` None on every skin removed borders | LibKa0s `430354d`, the GATE commits |
| ConsumableMaster stack count ignored the skin's shadow | `6e16ffe` |
| A title band drawn twice under `S.TitleBar` | LibKa0s `430354d`, SkinPaint minor 17 |
| Numeric list paths skipped silently in `Skin.FollowOnce` | LibKa0s `430354d` |
| One font object per string, hundreds on a grid | LibKa0s `430354d`, one per look |

## Test totals

From each repo's newest `docs/automated-tests` bundle, run on a clean tree. Each bundle's commit is one behind the branch head; the head only records that run. LibKa0s also ran as a release run. Lint is 0 warnings, 0 errors everywhere. Perf is as each manifest records it.

| Repo | Bundle | Commit | Passed | Failed | Skipped | Max CCN | Perf |
|---|---|---|---:|---:|---:|---:|---|
| LibKa0s | 20261101-195248 | d9a045a | 3902 | 0 | 3 | 15 | skip |
| AbsorbTracker | 20261101-201807 | 9e7cf8c | 1016 | 0 | 1 | 14 | pass |
| AuraMaster | 20261101-210026 | ce2e6cc | 2336 | 0 | 1 | 15 | pass |
| BankLedger | 20261101-202157 | 5895958 | 1629 | 0 | 1 | 15 | skip |
| ConsumableMaster | 20261101-202340 | 6e16ffe | 1387 | 0 | 1 | 15 | pass |
| DpsRace | 20261101-202803 | 6ba5c64 | 1352 | 0 | 1 | 15 | pass |
| DropWatcher | 20261101-203422 | 6074774 | 1927 | 0 | 1 | 15 | pass |
| KickCD | 20261101-201900 | b65518e | 1638 | 0 | 1 | 15 | pass |
| LibKa0sSkinTester | 20261101-201525 | d143651 | 858 | 0 | 1 | 14 | pass |
| LootHistory | 20261101-202413 | ed7a0d5 | 1954 | 0 | 1 | 15 | pass |
| MultiMeters | 20261101-210026 | 93c42e1 | 2533 | 0 | 1 | 15 | pass |
| PanelMaster | 20261101-201645 | a703eae | 1175 | 0 | 1 | 15 | skip |
| PartyFrameEnhanced | 20261101-210026 | a376cf8 | 633 | 0 | 1 | 14 | pass |
| PremadeGroupsFilterExtension | 20261101-201349 | e638513 | 516 | 0 | 1 | 14 | pass |
| PrettyChat | 20261101-201604 | ff8d62e | 672 | 0 | 1 | 15 | skip |
| QuickComms | 20261101-210705 | 32bf98d | 1710 | 0 | 1 | 15 | pass |
| WhatGroup | 20261101-203232 | ff48679 | 1082 | 0 | 1 | 15 | pass |
| **Total** | | | **26320** | **0** | **19** | | |

## The lead's own calls

These were not your rulings. Overturn any of them.

- **Preview and simulation re-look answered Current.** The release needs that answer; you did not give it. `checkpoints.tsv` M1 row and LibKa0s `CHANGELOG.md:149`.
- **The 42-dummy catalog is carried on this branch** though it has nothing to do with skinning (`RESUME.md`).

Addon agents made these calls and flagged them:

- DropWatcher's off-spec glow follows `sem.warband`, because the skin has one `glow.color`.
- MultiMeters' row stripe and marker use new owner tokens with alpha 0 under Ka0s Default, not `list.stripe` at 0.03, to keep the pixels.
- PartyFrameEnhanced spends schema v5 as an empty step (`a376cf8`), because the build that ran it stamped 5.

## Known limits

- **DropWatcher off-spec glow.** `sem.warband` is set only in `SkinDefs.lua` and M3 touched no `sem.*`, so the off-spec glow changes once on leaving Ka0s Default and is then the same in every skin.
- **Migrations overwrite player choices,** as you ruled: Thick outline flags go to From skin, and your KC and AM own fonts go behind their boxes (KC SKIN-36, AM SKIN-31).
- **Secret values.** `S.BarGloss` and the icon holder sit on bars that hold secrets in MultiMeters, and AuraMaster's gloss replays on a skin change in combat. Neither is proven outside a client (MM SKIN-33, SKIN-34; AM SKIN-41).
- **A client's `SetFontObject` color reset** is modeled, not observed. MultiMeters and DpsRace repaint after it for that reason.
- **Text shadow on 12.0.7.** The library says the client draws no shadow set on a string at runtime, so MultiMeters' old shadow may never have drawn. If so, the kept shadow is a visible change (MM SKIN-28).
- **AuraMaster icon borders on a live switch to WoW Default** stay flat until `/reload` (`80bb465`, SKIN-36).
- **MultiMeters under High Contrast:** the opaque row stripe is not walked by SKIN-39.
- **PGFE:** the panel's dropdown keeps its triangle while the skin picker draws a chevron. The arrow's rotation after a skin change is unproven (SKIN-41).
- **Perf.** KickCD's ms/iter rose in every scenario on a loaded machine (load average 17), with API counts and bytes flat. ConsumableMaster has no scenario for the bar's appearance pass, so its cost is unmeasured.
- **DropWatcher `modules/Window.lua`** is 1007 lines, past the 1000 band, accepted in its RESULTS with the tab strip named as the split.

## What could not be traced

- LibKa0s has no `docs/smoke-tests.md`, so the library has no check IDs of its own; it is smoked through the addons.
- The 42 dummies have no check in DpsRace's `docs/smoke-tests.md`. The first-section row has no ID.
- The agent digest has no section for AbsorbTracker or QuickComms, so their left-overs come from their commits and bundles.
- The Pending sign-off paragraphs omit checks this run re-opened: AbsorbTracker SKIN-1, 5, 6, 25, 41, 42 and MIGRATE-2; QuickComms SKIN-6 and FSKIN-12. `06_SMOKE_TESTS.md` was built from the diff against master as well as those paragraphs, and each of its 250 IDs was checked against that set.
- M3 has no `checkpoints.tsv` row because it is not pushed.

## What remains

1. You run `06_SMOKE_TESTS.md`, after a full client restart, and accept or reject the look changes in its section 3.
2. Failures get fixed on this branch, and results are copied into each addon's `docs/smoke-tests.md`.
3. On your go-ahead only: merge with `/dev-copilot:finalize` in dependency order, and push the v1.85.0 tag.
4. Bump nothing without your go-ahead.
