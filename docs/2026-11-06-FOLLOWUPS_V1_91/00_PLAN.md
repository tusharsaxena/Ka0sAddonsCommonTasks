# Follow-ups to the v1.90.0 run: line-chart pixels, LibKa0s peels, the dev-copilot placeholder bug (2026-11-06)

The owner asked to fix the three items left open in
`docs/2026-11-06-REVENDOR_LIBKA0S_V1_89/99_REPORT.md`. Branch in every touched repo:
`feat/2026-11-06-followups-v1-91`. No questions were needed. The owner's standing instructions are to
decide, use a checkpointed plan, push at milestones and merge only on go-ahead.

## 1. Line-chart lines (LibKa0s)

`WidgetsLineChart.lua` draws its axis (:400), grid (:414), markers (:427, :429), crosshair (:627) and
default series lines (:329) with `Line:SetThickness(1)`, which is 1 UI unit. These become one physical
pixel, re-sized on scale changes, through Core minor 16's pixel mechanism (`__PixelSize`,
`__WatchPixels`, `__OnPixelScale`), the same one v1.90.0's edges use. A host-passed series thickness
is read as physical pixels too. Consumers that draw a LineChart: LootHistory, LibKa0sSkinTester.

## 2. The four band files (LibKa0s)

As measured at v1.90.0: `LibKa0s/Core.lua` 1080, `LibKa0s/Widgets.lua` 1312,
`LibKa0s/SkinPaintExtras.lua` 1217 (its peel trigger has fired), and `tests/test_toast.lua` 1302. The
owner ruled "fix", so each is **peeled below 1000 lines along its own seam**, not ratified. The
seams:

- Core: the pixel-edge section (`__PixelSize` .. `__PixelBackdrop`).
- Widgets: the shared menu and cascade, or the dropdown/search box.
- SkinPaintExtras: the seam its census row names.
- test_toast: the stack cases.

Each new payload file carries its own `<NAME>_MINOR` and its shell's `NEEDS_*` floor, joins
`LibKa0s.xml` in load order, and is followed through `tests/majors.lua`, the `docs/api` documents,
`docs/releasing.md`'s file count, the band census and the register rows, which are closed. The peels
must not change behaviour: the existing suites pass unchanged, apart from file-path pins.

**A peel here is a release** (LibKa0s `CLAUDE.md`), so items 1 and 2 ship as **v1.91.0**. The tag is
cut locally and pushed only at the finalize. All 17 addons re-vendor it. A new payload file is a
blocker in any consumer whose `tests/loader.lua` (or a similar file) lists library files, and it is
fixed in that addon's re-vendor commit.

## 3. dev-copilot

- **The root cause of "Step 0 is broken"** is two bugs.
  - (a) The roster regex `\]\(\.\./\.\./…/\)` expects markdown links, but ADDONS.md writes
    `` `../../<Folder>/` ``.
  - (b) Claude Code substitutes `$1`, `$2`, … and `$ARGUMENTS` in `commands/*.md`, so every shell or
    awk positional in a command spec is replaced by the user's argument words. Measured:
    `commands/wow-revendor-libka0s.md:43,253` (`tag_at`'s `"$1"` / `"$2:CLAUDE.md"` arrived as
    `"Ka0s"` / `"repos:CLAUDE.md"`), and `commands/wow-revendor-standards.md:205-262` (the EOL check,
    11 hits). `$ARGUMENTS` itself is intended.
- **The fix:** no positional parameter in any command spec. Use named variables, or `awk -v`, or a
  script under `scripts/`. Fix the roster pattern everywhere a spec parses ADDONS.md, including
  `profiles/wow/agent-review.md:342`. Add a regression test in `scripts/` that fails on any
  `$<digit>` / `${<digit>}` in `commands/*.md`. Bump to **2.7.1** per its `CLAUDE.md`.
- **After the merge,** the owner updates the installed plugin and reloads, per the
  `use-installed-plugin` memory.

## Items, milestones, smoke

`plan-data/items.tsv` lists the items, and `plan-data/resume-state.sh` computes progress from git.

| Milestone | Contents | Push |
|---|---|---|
| M1 | FU-L1, FU-L2, FU-L3 in LibKa0s, and FU-DC1 in dev-copilot, each reviewed adversarially | branches pushed, tag still local |
| M2 | FU-RV-<X> in all 17 addons, each verified | branches pushed |
| FIN | owner smoke (`06_SMOKE_TESTS.md`), then on go-ahead the finalize: 20 repos merged `--no-ff`, master and tag v1.91.0 pushed, branches deleted | |

No addon version bumps. dev-copilot's 2.7.1 is a version-line change in its own repo, with no tag
(earlier runs left dev-copilot untagged).
