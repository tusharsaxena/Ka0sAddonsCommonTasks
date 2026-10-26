# Execution record: Ka0s Skin Tester (ST-01..ST-08)

Executed 2026-10-26 against [`00_DESIGN.md`](00_DESIGN.md) and [`01_PLAN.md`](01_PLAN.md), which stay as written.
Everything that differs from them is recorded here.

## Commits

| Id | Repo | Commit | Subject |
|---|---|---|---|
| ST-01 | LibKa0sSkinTester (`master`) | `50bf43b` | Scaffold Ka0s Skin Tester, born compliant |
| ST-01 | LibKa0sSkinTester (`master`) | `ae5bfed` | Record the first automated-test run (green, 455/1/456) |
| ST-02 | WowAddonStandards | `35e093e` | Add Ka0s Skin Tester to the addon roster |
| ST-03 | LibKa0sSkinTester | `5ec8bd0` | Skin owner and the swatch selector |
| ST-04 | LibKa0sSkinTester | `8d6f014` | The showroom window and its paint wrapper |
| ST-05 + ST-06 | LibKa0sSkinTester | `d580cb3` | Showroom sections for every paint primitive; value displays |
| ST-07 | LibKa0sSkinTester | `6071da3` | Sample settings page; /st collision reported once |
| ST-08 | LibKa0sSkinTester, this repo | see `git log` | Docs, smoke file, push |

ST-01 landed on the tester's `master`, the repo's first commits, and `master` was pushed when the owner
created the GitHub repo (`gh repo create` is refused to the agent by the auto-mode classifier, so the owner
ran it). Every later id is on `feat/2026-10-26-skin-tester`.

## Gate at the end

LibKa0sSkinTester: 482 passed / 1 skipped / 483 (the skip is the kit's diagnostics opt-out arm), luacheck
0 warnings / 0 errors over 66 files. WowAddonStandards: `scripts/check-standard.sh` all checks passed.

## Deviations from the plan and the design

- **Appearance tab kept (design).** The design dropped the tester's Appearance tab. Standard rule 24b requires
  a skin-adopting addon to carry it before Keybindings, so it stays on General. The swatch selector is the
  showroom's own picker beside it.
- **No `modules/SkinChoice.lua` (ST-03).** The scaffold's `core/SkinSetup.lua` already registers the owner and
  owns the read and write seams, and `NS.SkinChoice` is the Appearance tab's `get`. The pick is
  `NS.Selector.Pick(key)`: apply with `Skin:SetChoice`, save only on a change.
- **Unknown saved skin (ST-03).** `Skin:SetChoice` keeps any non-empty string, so the fallback to Ka0s Default
  is the addon's, in `NS.ApplySkinChoice`.
- **Dot functions (ST-04).** `Paint`, `AddSection` and `Caption` are dot functions like the rest of
  `NS.Showroom`, not the plan's colon methods. Two layout helpers joined them: `Grid` and `SampleButton`.
- **One commit for ST-05 + ST-06.** The coverage test cannot be green before the getters are on show, so the
  sections and the values landed together rather than leave a red commit between them.
- **Library widgets painted twice (ST-05).** `W.SearchBox`, `W.Dropdown` and `W.TestStrip` paint themselves
  through the owner's facade, which bypasses the showroom's record. Each is painted again through the wrapper:
  one target, one record, so the second paint costs nothing and the coverage claim stays honest.
- **Sample controls gained a sixth control (ST-07).** options-ui-§17 requires a class-color companion beside
  every color swatch, so the page carries Use class color (`classColorSource = "player"`).
- **`rowsForPage` filters by page (ST-07).** The scaffold handed every row to every page; a second page needed
  real filtering. A row with no `page` is General's.
- **The collision runs at OnEnable**, the addon's PLAYER_LOGIN. It scans `_G` once for another
  `SLASH_<NAME><n>` spelling `/st`. The help text and landing page still name `/st` afterwards (a Known
  Limitation in the tester's ARCHITECTURE.md).

## Found on the way

- The scaffold came from WhatGroup, and its test tree still carried WhatGroup's popup, group-finder, teleport,
  cooldown and chat-link mocks and perf scenarios. They were stripped in ST-01, and the offline perf runner
  was rewritten for the showroom's own paths.
- The bulk rename had turned WhatGroup's issue and finding ids into tester ids that do not exist. They point
  back to WhatGroup again (`WhatGroup#22`, `WhatGroup WG-26`).
- Comment citations still inherited from WhatGroup (a `docs/midnight-quirks.md` this repo does not have, a
  `core/Compat.lua` it does not ship, a `tests/prose_waivers.lua` the scaffold rule says a new addon does not
  need) were reported by the ST-08 doc sync and left for the owner's call.

## Owner smoke

2026-10-26, the owner, in game: "Skin test works great! ship it. go ahead and merge". Recorded as the
owner's verdict on the run; the per-row Result cells in `02_SMOKE_TESTS.md` stay the owner's to fill.

## Finalize

Merged on the owner's go-ahead (same message, 2026-10-26) with `/dev-copilot:finalize`: WowAddonStandards,
then LibKa0sSkinTester, then this repo, each `--no-ff` into `master`, pushed, and the feature branch
deleted. No tag, no version bump.

## Open

- Later, from the owner's feedback of 2026-10-26: the Azeroth, Glass, Obsidian, High Contrast and Midnight
  skin fixes; renaming Appearance to Styles; the scope (everything vs the main window) and font settings.
