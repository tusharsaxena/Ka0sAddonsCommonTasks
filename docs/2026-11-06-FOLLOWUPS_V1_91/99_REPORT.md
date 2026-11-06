# Report: the v1.91.0 follow-ups (2026-11-06)

The owner asked to fix the three items left open by `docs/2026-11-06-REVENDOR_LIBKA0S_V1_89/99_REPORT.md`.
Owner smoke SM-1 and SM-2 passed in game on 2026-11-06, and the owner then gave the go-ahead to finalize.

## What landed

| Item | Repo | Outcome |
|---|---|---|
| FU-L1 | LibKa0s | The line chart's axis, grid, markers, crosshair and series lines are one physical pixel at any UI scale (WidgetsLineChart minor 7). The area fill's columns stay in UI units on purpose: they are spacing, not lines. |
| FU-L2 | LibKa0s | Peeled with no behaviour change. Core.lua 1080 -> 949 (new CorePixel.lua). Widgets.lua 1312 -> 559 (new WidgetsDropdown.lua: the dropdown and shared menu, because the search-box seam alone left about 1208). SkinPaintExtras.lua 1217 -> 922 (new SkinAceConfirm.lua and SkinPaintHud.lua, because the census seam alone left about 1058). tests/test_toast.lua 1302 -> 760 (new test_toast_stack.lua and fixture_toast.lua). The band census is down to thirteen files, none over 1500. |
| FU-L3 | LibKa0s | Release **v1.91.0**, tag pushed at the finalize. |
| FU-RV-x17 | every addon | Re-vendored to v1.91.0. Any loader list that names library files gained the new payload files. Every gate 0 failed. |
| FU-DC1 | dev-copilot | **2.7.1** (no tag, like earlier runs). No `$<digit>` positional in any `commands/*.md`: Claude Code had been substituting the user's argument words into `wow-revendor-libka0s`'s `tag_at` and `wow-revendor-standards`' EOL check. The ADDONS.md roster pattern now matches its backticked table cells. The line-ending stray count is NUL-safe and identical in the command and the audit agent. `scripts/test_command_specs.py` (7 cases) guards all three. It took two review rounds: stale citations and counts, then a newline-in-filename double count. |
| FIN | all 20 | Content-only sync-docs, `--no-ff` merges each gated on the merge result (vendor drift 0), master pushed, branches deleted locally and on origin. |

Commits are in `checkpoints.tsv`.

## For the owner

- **Update and reload the dev-copilot plugin**, so the fixed commands are the ones that run. The
  installed copy is still 2.7.0.
- **Line-ending stray count:** it still counts a binary file that `.gitattributes` does not mark
  `binary` and that contains CR bytes. That behaviour comes from master, and in practice the
  collection marks its binaries.
- **Default series line width:** it is now 1.5 physical pixels. At the owner's UI scale it used to
  draw at about 1.8 px.
